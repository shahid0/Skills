# Usage Example: Test Run and Self-Healing Loop

This example demonstrates how to use the `self-heal-tests` skill to automatically run a project's test suite, extract failing test details from the `.xcresult` bundle, and use that structured feedback to self-correct a bug in the code.

---

## 1. Scenario: The Calculator Division Bug

### Target Code (`Calculator.swift`)
```swift
import Foundation

public struct Calculator {
    public func divide(_ a: Double, _ b: Double) -> Double {
        // BUG: Does not check for division by zero
        return a / b
    }
}
```

### Unit Test (`CalculatorTests.swift`)
```swift
import XCTest
@testable import Calculator

final class CalculatorTests: XCTestCase {
    func testDivideByZero() throws {
        let calc = Calculator()
        // We expect division by zero to yield Double.nan, but instead let's say the specification requires
        // the function to return a specific default or handle it safely (or throw an error).
        // Let's assume the test asserts that dividing by zero returns a specific error or safe value,
        // but it currently fails because the test checks for an explicit throwing behavior or custom exception.
        
        XCTAssertTrue(calc.divide(10.0, 0.0).isNaN, "Division by zero should result in NaN or throw an error based on spec.")
    }
}
```

---

## 2. Running the Parser Script

The agent runs the `xcresult_parser.py` script to run the tests and generate a report:

```bash
scripts/xcresult_parser.py \
  --project ./Calculator/Calculator.xcodeproj \
  --scheme Calculator \
  --destination "platform=macOS" \
  --output-report ./build/test_report.json \
  --export-attachments-dir ./build/Attachments
```

---

## 3. Parsed Output JSON Report (`test_report.json`)

The script outputs a clean JSON report containing exact failure context:

```json
{
  "status": "failed",
  "summary": {
    "total_tests": 5,
    "passed_tests": 4,
    "failed_tests": 1,
    "skipped_tests": 0
  },
  "failures": [
    {
      "test_case_name": "CalculatorTests.testDivideByZero()",
      "message": "XCTAssertTrue failed - Division by zero should result in NaN or throw an error based on spec.",
      "file_path": "Tests/CalculatorTests.swift",
      "line_number": 10,
      "url": "Tests/CalculatorTests.swift#CharacterRangeLen=0&EndingLineNumber=9&StartingLineNumber=9",
      "screenshots": [
        {
          "file_name": "CalculatorTests_testDivideByZero_1_Failure.png",
          "path": "build/Attachments/CalculatorTests_testDivideByZero_1_Failure.png",
          "name": "Failure Screenshot",
          "device_name": "MacBook Pro",
          "device_id": "LOCAL-MAC-ID"
        }
      ]
    }
  ],
  "xcodebuild_exit_code": 65,
  "error_message": null
}
```

---

## 4. The Self-Healing Workflow (Executed by the Agent)

### Step 1: Read the failure details
The agent inspects the `test_report.json` and extracts:
- Failing file: `Tests/CalculatorTests.swift` at line 10.
- Message: `XCTAssertTrue failed - Division by zero should result in NaN or throw an error based on spec.`
- Underlying class: `CalculatorTests`, test: `testDivideByZero()`.

### Step 2: Read target code and identify bug
The agent reads `Calculator.swift` and determines that `a / b` when `b == 0` does not throw or return `Double.nan` as expected by the spec, or it needs a safety guard:

```swift
// Target Code with guard added
public struct Calculator {
    public func divide(_ a: Double, _ b: Double) -> Double {
        if b == 0.0 {
            return Double.nan
        }
        return a / b
    }
}
```

### Step 3: Apply the fix
The agent uses a file editing tool (like `replace_file_content`) to apply the fix to `Calculator.swift`.

### Step 4: Re-run verification tests
The agent runs the `xcresult_parser.py` command again:

```bash
scripts/xcresult_parser.py \
  --project ./Calculator/Calculator.xcodeproj \
  --scheme Calculator \
  --destination "platform=macOS" \
  --output-report ./build/test_report.json
```

Output:
```text
============================================================
TEST SUITE STATUS: PASSED
============================================================
Total Tests:   5
Passed:        5
Failed:        0
Skipped:       0
============================================================
```

The test suite now passes, indicating a successful self-heal!
