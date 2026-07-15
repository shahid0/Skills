# Standard xctrace Profiling Templates and Metrics

This reference lists the primary `xctrace` templates available on macOS and iOS, along with their key performance metrics, data schemas, and typical use cases.

## Core Templates

### 1. Time Profiler
*   **Template Name:** `Time Profiler`
*   **Description:** Performs CPU thread-sampling at regular intervals (typically 1ms) to build a statistical picture of where applications spend CPU time.
*   **Key Schemas:**
    *   `time-profile`: Aggregated stack traces with time weights.
    *   `time-sample`: Raw individual thread samples.
*   **Primary Metrics:**
    *   **CPU Weight (Time):** Total duration spent in a call tree path.
    *   **Self Time (Exclusive Time):** Time spent executing code inside the leaf function itself.
    *   **Inclusive Time:** Total time spent inside the function and all its children.
*   **Best For:** Finding CPU bottlenecks, hotspots, and UI hangs.

### 2. Allocations
*   **Template Name:** `Allocations`
*   **Description:** Tracks the lifecycle of all heap allocations, object creations, and deallocations.
*   **Key Schemas:**
    *   `allocations`: Heap allocation event log.
*   **Primary Metrics:**
    *   **All Heap Allocations:** Cumulative count and size of all heap objects allocated.
    *   **Persistent Bytes:** Memory currently occupied by active objects on the heap.
    *   **Allocation Density:** Rate of allocation over time.
*   **Best For:** Analyzing memory growth, optimizing object reuse, and reducing heap overhead.

### 3. Leaks
*   **Template Name:** `Leaks`
*   **Description:** Scans the heap periodically to detect memory that has no references but has not been freed.
*   **Key Schemas:**
    *   `leaks`: Leak detection events and leak backtraces.
*   **Primary Metrics:**
    *   **Leak Count:** Number of unreachable heap allocations.
    *   **Leaked Bytes:** Total memory leaked.
*   **Best For:** Finding retain cycles, unmanaged C/C++ memory leaks, and Swift/Dart object leaks.

### 4. SwiftUI
*   **Template Name:** `SwiftUI`
*   **Description:** Profiles SwiftUI-specific runtime performance, including view body evaluations, state updates, and rendering pipelines.
*   **Key Schemas:**
    *   `swiftui-view-lifetimes`: View body evaluation counts and durations.
*   **Primary Metrics:**
    *   **Body Evaluation Count:** Number of times a SwiftUI view's `body` property is evaluated.
    *   **Body Duration:** Time spent inside view body evaluation.
*   **Best For:** Diagnosing excessive SwiftUI view updates, slow body evaluations, and rendering hitches.

### 5. Swift Concurrency
*   **Template Name:** `Swift Concurrency`
*   **Description:** Tracks Swift cooperative thread pool activity, actor execution, and asynchronous task lifecycles.
*   **Key Schemas:**
    *   `swift-concurrency`: Cooperative pool state, task creations, suspensions, and actor hop records.
*   **Primary Metrics:**
    *   **Task Suspend Duration:** Total time async tasks spend suspended.
    *   **Actor Hops:** Count of context switches between actors.
    *   **Cooperative Thread Count:** Number of active threads in the concurrency pool.
*   **Best For:** Diagnosing concurrency bottlenecks, actor contention, thread pool starvation, and execution delays.

### 6. Animation Hitches
*   **Template Name:** `Animation Hitches`
*   **Description:** Monitors frame rates, rendering pipelines, and Core Animation transactions to pinpoint visual stutter.
*   **Key Schemas:**
    *   `hitch-intervals`: Render loop frame intervals and hitch times.
*   **Primary Metrics:**
    *   **Hitch Time:** Delay in presenting a frame relative to the target frame rate.
    *   **Hitch Rate:** Total hitch time divided by test duration (ms/s).
*   **Best For:** Diagnosing UI stutter, layout overhead, and frame drops.

### 7. App Launch
*   **Template Name:** `App Launch`
*   **Description:** Details the startup process of an application, from process invocation (`exec`) to the presentation of the first frame.
*   **Key Schemas:**
    *   `app-launch-phases`: Subsections of launch (pre-main, dyld, static initializers, UIKit/SwiftUI init).
*   **Primary Metrics:**
    *   **Time to First Frame:** Elapsed time until the UI is responsive.
    *   **Static Initializer Time:** Time spent executing static initializers.
*   **Best For:** Optimizing startup times and identifying slow initializers.

## Complete Template List

To get the exact list of templates supported by your local Xcode installation, execute:

```bash
xcrun xctrace list templates
```
