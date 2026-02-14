---
name: performance-optimize
description: Analyze and optimize code performance - slow execution, high memory usage, performance tuning.
---

## Analysis Flow

### 1. Locate Bottleneck
- Time complexity analysis (O(n) vs O(n²))
- Space complexity analysis
- I/O bottleneck (file/network/database)
- Hot function identification

### 2. Common Strategies
- **Algorithm**: Better data structure/algorithm
- **Cache**: Cache repeated computation results
- **Batch**: Merge many small operations into one large operation
- **Lazy load**: Defer initialization, load on demand
- **Concurrent**: Parallelize independent tasks
- **Reduce allocation**: Object pool/reuse/avoid frequent GC

### 3. Language-Specific
- **Kotlin/Java**: Avoid boxing, use sequences, coroutines
- **JavaScript**: Avoid reflows, virtual scrolling, Web Workers
- **Python**: List comprehensions, numpy vectorization, generators
- **SQL**: Index optimization, avoid SELECT *, batch operations

### 4. Verify
- Before/after comparison data
- Ensure optimization didn't introduce bugs
