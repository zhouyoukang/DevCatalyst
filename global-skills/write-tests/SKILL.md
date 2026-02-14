---
name: write-tests
description: Write unit tests and integration tests - add tests, verify correctness, improve coverage.
---

## Test Principles
- Each test verifies one thing
- Name describes expected behavior: `should_returnError_when_inputIsNull`
- AAA pattern: Arrange → Act → Assert
- Test independence: no execution order dependency

## Test Types
- **Unit test**: Single function/class, mock external deps
- **Integration test**: Module interactions
- **E2E test**: Complete user flow

## Frameworks
| Language | Framework | Command |
|----------|-----------|--------|
| Kotlin/Java | JUnit5 + MockK | `./gradlew test` |
| JavaScript | Jest / Vitest | `npm test` |
| Python | pytest | `pytest` |
| Go | testing | `go test ./...` |

## Template (JUnit5 + Kotlin)
```kotlin
@Test
fun `should return empty when input is blank`() {
    // Arrange
    val input = ""
    // Act
    val result = myFunction(input)
    // Assert
    assertEquals(emptyList(), result)
}
```

## Must Cover
- Happy path
- Boundary conditions (null, zero, max)
- Error paths (exceptions, invalid input)
- Concurrency (if applicable)
