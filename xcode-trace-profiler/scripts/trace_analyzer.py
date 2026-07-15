#!/usr/bin/env python3
"""
trace_analyzer.py
A wrapper and parser script for xctrace. Records performance traces,
exports them to XML, and parses the XML to highlight CPU/performance bottlenecks.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def resolve_element(elem, id_map):
    """
    Dereference elements using the 'ref' attribute.
    If the element has a 'ref' attribute, look up the referenced element in the id_map.
    Otherwise, return the element itself.
    """
    if elem is None:
        return None
    ref = elem.attrib.get('ref')
    if ref:
        return id_map.get(ref, elem)
    return elem


def find_xpath_from_toc(toc_xml_str, schema_name):
    """
    Parses the Table of Contents XML and finds the XPath for the requested schema.
    """
    try:
        root = ET.fromstring(toc_xml_str)
        for run in root.findall('.//run'):
            run_num = run.attrib.get('number', '1')
            for data in run.findall('data'):
                for table in data.findall('table'):
                    if table.attrib.get('schema') == schema_name:
                        return f'/trace-toc/run[@number="{run_num}"]/data/table[@schema="{schema_name}"]'
    except Exception as e:
        sys.stderr.write(f"Warning: Failed to parse TOC XML: {e}\n")
    return None


def run_command(cmd, desc="command"):
    """
    Executes a system command and returns the completed process.
    """
    sys.stderr.write(f"Running {desc}: {' '.join(cmd)}\n")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error running {desc}:\nExit code: {e.returncode}\n")
        sys.stderr.write(f"Stdout: {e.stdout}\n")
        sys.stderr.write(f"Stderr: {e.stderr}\n")
        raise e


def record_trace(template, output_path, launch_args=None, attach=None, time_limit=None, device=None):
    """
    Executes xcrun xctrace record.
    """
    cmd = ["xcrun", "xctrace", "record"]
    cmd += ["--template", template]
    cmd += ["--output", output_path]

    if device:
        cmd += ["--device", device]
    if time_limit:
        cmd += ["--time-limit", time_limit]

    if attach:
        cmd += ["--attach", str(attach)]
    elif launch_args:
        cmd += ["--launch", "--"] + launch_args
    else:
        raise ValueError("Must specify either --launch or --attach to record a trace")

    # Run xctrace record. This will wait for process exit or time limit.
    run_command(cmd, "xctrace record")


def export_toc(trace_path):
    """
    Exports the table of contents of the trace file.
    """
    cmd = ["xcrun", "xctrace", "export", "--input", trace_path, "--toc"]
    res = run_command(cmd, "xctrace export TOC")
    return res.stdout


def export_xpath(trace_path, xpath, output_xml_path):
    """
    Exports data targeting the specified XPath from the trace file.
    """
    cmd = ["xcrun", "xctrace", "export", "--input", trace_path, "--xpath", xpath, "--output", output_xml_path]
    run_command(cmd, "xctrace export data")


def parse_trace_xml(xml_path):
    """
    Parses the exported XML and aggregates CPU self & inclusive time.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Build ID registry for all elements with 'id'
    id_map = {}
    for elem in root.iter():
        elem_id = elem.attrib.get('id')
        if elem_id:
            id_map[elem_id] = elem

    functions = {}
    total_weight = 0
    samples_count = 0

    # Search for all rows in the trace query results
    for row in root.findall('.//row'):
        samples_count += 1

        # Extract sample weight (CPU duration in nanoseconds)
        weight_elem = row.find('weight')
        if weight_elem is not None:
            weight_elem = resolve_element(weight_elem, id_map)
            try:
                weight = int(weight_elem.text.strip())
            except (ValueError, AttributeError):
                weight = 0
        else:
            weight = 0

        total_weight += weight

        # Extract backtrace
        tb_elem = row.find('tagged-backtrace')
        if tb_elem is not None:
            tb_elem = resolve_element(tb_elem, id_map)
            bt_elem = tb_elem.find('backtrace')
            if bt_elem is not None:
                bt_elem = resolve_element(bt_elem, id_map)
                frames = bt_elem.findall('frame')

                resolved_frames = []
                for f in frames:
                    rf = resolve_element(f, id_map)
                    name = rf.attrib.get('name', 'Unknown')
                    addr = rf.attrib.get('addr', '0x0')

                    # Find binary info
                    binary_name = 'Unknown'
                    bin_elem = rf.find('binary')
                    if bin_elem is not None:
                        bin_elem = resolve_element(bin_elem, id_map)
                        binary_name = bin_elem.attrib.get('name', 'Unknown')

                    resolved_frames.append({
                        'name': name,
                        'addr': addr,
                        'binary': binary_name
                    })

                if resolved_frames:
                    # Leaf frame represents where the CPU was actually executing (Self Time)
                    leaf = resolved_frames[0]
                    leaf_name = leaf['name']
                    if leaf_name not in functions:
                        functions[leaf_name] = {
                            'self_weight': 0,
                            'inclusive_weight': 0,
                            'binary': leaf['binary'],
                            'samples_count': 0
                        }
                    functions[leaf_name]['self_weight'] += weight
                    functions[leaf_name]['samples_count'] += 1

                    # All unique frames in backtrace represent parent callers (Inclusive Time)
                    seen_in_bt = set()
                    for f in resolved_frames:
                        f_name = f['name']
                        if f_name in seen_in_bt:
                            continue
                        seen_in_bt.add(f_name)

                        if f_name not in functions:
                            functions[f_name] = {
                                'self_weight': 0,
                                'inclusive_weight': 0,
                                'binary': f['binary'],
                                'samples_count': 0
                            }
                        functions[f_name]['inclusive_weight'] += weight

    return functions, total_weight, samples_count


def generate_report(functions, total_weight, samples_count, top_n=20, min_pct=0.0):
    """
    Sorts, filters, and formats the parsed trace data.
    """
    report_list = []
    for name, stats in functions.items():
        self_pct = (stats['self_weight'] / total_weight * 100) if total_weight > 0 else 0.0
        inc_pct = (stats['inclusive_weight'] / total_weight * 100) if total_weight > 0 else 0.0

        if self_pct < min_pct and inc_pct < min_pct:
            continue

        report_list.append({
            'name': name,
            'binary': stats['binary'],
            'self_weight_ns': stats['self_weight'],
            'self_weight_ms': stats['self_weight'] / 1e6,
            'self_pct': self_pct,
            'inclusive_weight_ns': stats['inclusive_weight'],
            'inclusive_weight_ms': stats['inclusive_weight'] / 1e6,
            'inclusive_pct': inc_pct,
            'samples_count': stats['samples_count']
        })

    # Sort primarily by Self Time, then by Inclusive Time
    report_list.sort(key=lambda x: (x['self_weight_ns'], x['inclusive_weight_ns']), reverse=True)

    return {
        'total_weight_ns': total_weight,
        'total_weight_ms': total_weight / 1e6,
        'total_samples': samples_count,
        'top_functions': report_list[:top_n]
    }


def print_text_report(report_data):
    """
    Prints a clean, human-readable terminal table of CPU usage.
    """
    print("=" * 110)
    print(f"XCTRACE CPU PROFILE REPORT")
    print(f"Total Samples: {report_data['total_samples']}")
    print(f"Total CPU Time: {report_data['total_weight_ms']:.2f} ms")
    print("=" * 110)
    print(f"{'Function Name':<50} | {'Binary':<15} | {'Self Time':<15} | {'Inclusive Time':<15} | {'Samples':<8}")
    print("-" * 110)

    for fn in report_data['top_functions']:
        name = fn['name']
        if len(name) > 48:
            name = name[:45] + "..."

        binary = fn['binary']
        if len(binary) > 13:
            binary = binary[:11] + "..."

        self_str = f"{fn['self_weight_ms']:.2f} ms ({fn['self_pct']:.1f}%)"
        inc_str = f"{fn['inclusive_weight_ms']:.2f} ms ({fn['inclusive_pct']:.1f}%)"

        print(f"{name:<50} | {binary:<15} | {self_str:<15} | {inc_str:<15} | {fn['samples_count']:<8}")
    print("=" * 110)


def main():
    parser = argparse.ArgumentParser(description="xctrace profiling and analysis script.")

    # Source options (Record or Input Trace)
    parser.add_argument("--input-trace", help="Path to an existing .trace file to analyze (skips recording)")

    # Recording options
    parser.add_argument("-t", "--template", default="Time Profiler", help="xctrace template to record with")
    parser.add_argument("-o", "--output", help="Output path for recorded trace file (e.g. recording.trace)")
    parser.add_argument("-l", "--launch", nargs=argparse.REMAINDER, help="Executable and arguments to launch (must be at the end)")
    parser.add_argument("-a", "--attach", help="Process ID or name to attach to")
    parser.add_argument("-d", "--device", help="Target device name or UDID")
    parser.add_argument("--time-limit", help="Limit recording time (e.g., 5s, 5000ms)")

    # Exporting and Parsing options
    parser.add_argument("--xpath", help="Custom XPath schema query to export (skips TOC lookup)")
    parser.add_argument("--export-only", action="store_true", help="Only record/export, do not analyze")
    parser.add_argument("--xml-path", help="Path to save exported XML file (defaults to temp file)")
    parser.add_argument("--top", type=int, default=20, help="Number of top functions to display")
    parser.add_argument("--min-pct", type=float, default=0.1, help="Minimum self/inclusive percentage to show")
    parser.add_argument("--json", action="store_true", help="Output final analysis report as JSON")

    args = parser.parse_args()

    # Determine trace file path
    trace_path = args.input_trace
    temp_trace_dir = None

    if not trace_path:
        # We need to record a new trace
        if not args.launch and not args.attach:
            parser.error("Must provide either --input-trace or at least one of --launch/--attach for recording")

        if args.output:
            trace_path = args.output
        else:
            temp_trace_dir = tempfile.TemporaryDirectory(suffix=".trace")
            trace_path = os.path.join(temp_trace_dir.name, "recording.trace")

        try:
            record_trace(
                template=args.template,
                output_path=trace_path,
                launch_args=args.launch,
                attach=args.attach,
                time_limit=args.time_limit,
                device=args.device
            )
        except Exception as e:
            sys.stderr.write(f"Recording failed: {e}\n")
            if temp_trace_dir:
                temp_trace_dir.cleanup()
            sys.exit(1)

    # Now we have trace_path
    if not os.path.exists(trace_path):
        sys.stderr.write(f"Error: Trace file not found at {trace_path}\n")
        sys.exit(1)

    # Determine XML export path
    temp_xml_file = None
    xml_path = args.xml_path
    if not xml_path:
        temp_xml_file = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        xml_path = temp_xml_file.name
        temp_xml_file.close()

    try:
        # Determine XPath
        xpath = args.xpath
        if not xpath:
            # Load TOC
            toc_xml = export_toc(trace_path)
            # Standard schemas in order of preference
            target_schemas = ["time-profile", "time-sample", "cpu-profile"]
            for schema in target_schemas:
                xpath = find_xpath_from_toc(toc_xml, schema)
                if xpath:
                    sys.stderr.write(f"Auto-detected schema: '{schema}' using XPath: {xpath}\n")
                    break

            if not xpath:
                raise ValueError("Could not find a supported time/CPU profile schema in trace Table of Contents. Try specifying --xpath manually.")

        # Export table data to XML
        export_xpath(trace_path, xpath, xml_path)

        if args.export_only:
            print(f"Data exported successfully to: {xml_path}")
            return

        # Parse XML
        sys.stderr.write("Parsing exported XML data...\n")
        functions, total_weight, samples_count = parse_trace_xml(xml_path)

        if total_weight == 0:
            sys.stderr.write("Warning: Total CPU weight is 0. Check if application was active during trace.\n")

        # Generate report
        report_data = generate_report(
            functions=functions,
            total_weight=total_weight,
            samples_count=samples_count,
            top_n=args.top,
            min_pct=args.min_pct
        )

        # Output results
        if args.json:
            print(json.dumps(report_data, indent=2))
        else:
            print_text_report(report_data)

    finally:
        # Cleanup temporary files
        if temp_xml_file and os.path.exists(xml_path):
            os.remove(xml_path)
        if temp_trace_dir:
            temp_trace_dir.cleanup()


if __name__ == "__main__":
    main()
