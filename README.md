# Lab 5: Static Code Analysis

## Known Issue Table

| Issue # | Issue | Type | Line(s) | Tool | Severity | Error Code | Description | Fix Approach |
|:-------:|-------|------|:-------:|------|:--------:|------------|-------------|--------------|
| 1 | Mutable default argument | Bug | 8 | Pylint | **HIGH** | W0102 | `logs=[]` shared across all function calls | Changed default to `logs=None` and initialize inside function |
| 2 | Use of eval() | Security | 59 | Bandit | **HIGH** | B307 | `eval()` can execute arbitrary code | Removed `eval()` entirely |
| 3 | Bare except clause | Bug | 19 | Pylint, Flake8 | **HIGH** | W0702, E722 | Catches all exceptions including system exits | Replaced with specific exception types |
| 4 | Try-except-pass pattern | Bug | 19-20 | Bandit | MEDIUM | B110 | Silently ignores all errors | Added proper exception handling |
| 5 | No input validation | Bug | 8, 14 | Manual | **HIGH** | N/A | Functions accept invalid types causing crashes | Added type checking with `isinstance()` |
| 6 | Unused import | Clean Code | 2 | Pylint, Flake8 | LOW | W0611, F401 | `logging` module imported but never used | Removed unused import |
| 7 | File not using context manager | Bug | 26, 32 | Pylint | MEDIUM | R1732 | Files may not close properly on errors | Replaced with `with open()` statement |
| 8 | No encoding specified | Bug | 26, 32 | Pylint | MEDIUM | W1514 | File operations without encoding can fail | Added `encoding='utf-8'` parameter |
| 9 | Global statement usage | Design | 6, 27 | Pylint | MEDIUM | W0603 | Using global variables makes code hard to test | Refactored to class-based structure |
| 10 | Old string formatting | Style | 12 | Pylint | LOW | C0209 | Using `%s` formatting instead of f-strings | Replaced with f-strings |
| 11 | Missing module docstring | Quality | 1 | Pylint | LOW | C0114 | No module-level documentation | Added comprehensive module docstring |
| 12 | Missing function docstrings | Quality | 8,14,22,25,31,36,41,48 | Pylint | LOW | C0116 | No function documentation | Added docstrings to all functions |
| 13 | Non-snake_case names | Style | 8,14,22,25,31,36,41 | Pylint | LOW | C0103 | Functions use camelCase | Renamed to snake_case |
| 14 | Missing blank lines | Style | Multiple | Flake8 | LOW | E302, E305 | PEP 8 requires 2 blank lines | Added proper spacing |
| 15 | Negative quantity allowed | Logic | 49 | Manual | MEDIUM | N/A | Allows negative stock levels | Added validation for negative values |
| 16 | No error handling for missing items | Bug | 22-23 | Manual | MEDIUM | N/A | `getQty()` crashes with KeyError | Added explicit KeyError check |

## Reflection Questions

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest to Fix:**

The style-related issues were by far the easiest to address:

- **Blank line spacing** (E302, E305) - These were purely mechanical changes requiring simply adding two blank lines between functions. No logic understanding was needed.
- **String formatting** (C0209) - Converting from `%s` formatting to f-strings was straightforward: `"%s: Added %d" % (time, qty)` became `f"{time}: Added {qty}"`.
- **Unused imports** (W0611) - Simply deleting `import logging` was trivial once identified.
- **Function naming** (C0103) - While tedious, renaming functions from camelCase to snake_case was conceptually simple with IDE refactoring tools.

**Hardest to Fix:**

The conceptual and architectural issues required deeper understanding:

- **Mutable default argument (W0102)** - This was the most challenging because it required understanding Python's evaluation model. I had to learn that `def addItem(logs=[])` creates the list **once** at function definition time, not at call time, meaning all function calls share the same list object. The fix was simple once I understood the problem, but grasping why it's dangerous took research.

- **Global variable refactoring (W0603)** - Converting from a global `stock_data` dictionary to a class-based structure required rethinking the entire program architecture. I had to understand object-oriented principles, decide on class methods vs. instance methods, and ensure state management worked correctly.

- **Comprehensive input validation** - This required anticipating all possible edge cases: What if someone passes a number as an item name? What about negative quantities? Empty strings? The challenge was thinking through all failure modes and deciding on appropriate error types (`ValueError` vs `TypeError`).

- **Replacing eval() (B307)** - While removing the line was simple, understanding why it's dangerous required learning about code injection vulnerabilities. I researched how malicious input could delete an entire system, transforming a simple fix into a valuable security lesson.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

The tools were remarkably accurate overall, with very few debatable warnings:

**Mostly Legitimate Warnings:**

All the high and medium severity issues were genuine problems that needed fixing. The security vulnerabilities (eval usage, bare exceptions) were absolutely critical, and the logic bugs (mutable defaults, missing validation) caused real runtime issues.

**Potentially Debatable Cases:**

- **Snake_case naming convention (C0103)**: Pylint flagged all camelCase function names like `addItem`, `removeItem`, etc. While this violates PEP 8 style guidelines, the original names were perfectly valid Python code that would run without issues. Whether this is a "false positive" depends on perspective—it's not a bug, but it does violate Python community standards. For a personal script, camelCase would be fine; for a team project or library, following PEP 8 is essential for consistency. I chose to fix these because following conventions makes code more maintainable and familiar to other Python developers.

- **Global statement warning (W0603)**: Pylint warns against using `global stock_data`, and while globals are generally discouraged, for a simple 60-line script, using a global dictionary isn't necessarily "wrong"—just not best practice. However, refactoring to a class made the code significantly more testable and reusable, so this warning was valuable despite being somewhat subjective for small scripts.

- **Line length violations (E501)**: Flake8's strict 79-character limit flagged several lines. In modern development with wide monitors, many teams use 100 or even 120 character limits. However, 79 characters ensures code is readable in split-screen editors, diff views, and code review tools.

**No True False Positives:**

Importantly, none of the tools flagged correct code as incorrect. Every warning either represented a genuine issue (bug, security risk) or a legitimate style concern (PEP 8 violation). The tools proved highly accurate for Python code analysis.

### 3. How would you integrate static analysis tools into your actual software development workflow?

I would implement static analysis at multiple stages of the development lifecycle:

**Local Development (Pre-Commit):**

- **IDE Integration**: Configure VS Code or PyCharm to run linters in real-time, showing warnings as I type. This catches issues immediately when they're cheapest to fix.

- **Pre-commit Hooks**: Use Git pre-commit hooks to automatically run checks before allowing commits:
  ```bash
  #!/bin/bash
  # .git/hooks/pre-commit
  python -m pylint *.py --fail-under=8.0
  python -m flake8 *.py --max-line-length=100
  python -m bandit -r . -ll
  
  if [ $? -ne 0 ]; then
    echo "Linting failed. Fix issues before committing."
    exit 1
  fi
  ```
  This prevents committing code with serious issues, maintaining clean commit history.

- **Configuration Files**: Create `.pylintrc`, `.flake8`, and `.bandit` configuration files in the repository to standardize rules across the team.

**Continuous Integration Pipeline:**

Integrate into GitHub Actions or GitLab CI to run on every pull request:

```yaml
name: Code Quality Checks

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pylint flake8 bandit
      
      - name: Run Pylint
        run: |
          pylint src/ --fail-under=8.0 --output-format=colorized
        continue-on-error: false
      
      - name: Run Flake8
        run: |
          flake8 src/ --max-line-length=100 --statistics
      
      - name: Run Bandit (Security)
        run: |
          bandit -r src/ -f json -o bandit-report.json
          bandit -r src/ -ll
      
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: code-quality-reports
          path: bandit-report.json
```

**Code Review Process:**

- Require all linting checks to pass before allowing pull request merges
- Display linting results as comments on pull requests automatically
- Use tools like CodeClimate or SonarQube to track code quality trends over time

**Quality Gates:**

- Block deployments to production if Pylint score falls below 8.0
- Fail builds on any high-severity Bandit security issues
- Track technical debt by monitoring linting warnings over time

**Incremental Adoption for Legacy Code:**

For existing codebases with many violations:
1. Start with security checks (Bandit) - fix critical vulnerabilities first
2. Add Flake8 for new files only - prevent new style violations
3. Gradually increase Pylint threshold (7.0 → 8.0 → 9.0) as code improves
4. Use `# pylint: disable=rule-name` sparingly for unavoidable exceptions with comments explaining why

This multi-layered approach catches issues early (IDE), prevents bad commits (pre-commit hooks), and ensures quality in production (CI/CD).

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The improvements were substantial across multiple dimensions:

**Security Improvements:**

- **Eliminated code injection vulnerability**: Removing `eval()` means the application is now safe from arbitrary code execution attacks. The original code could have executed malicious commands if user input ever reached that eval statement.
- **Removed insecure patterns**: Replacing bare `except:` clauses prevents accidentally catching and hiding security exceptions, making the code more auditable.

**Reliability and Robustness:**

- **Input validation prevents crashes**: The original code crashed with `TypeError: unsupported operand type(s) for +: 'int' and 'str'` when called with invalid arguments. Now, the code validates inputs early and provides clear error messages like "Item must be a string, got int" instead of cryptic tracebacks.

- **Specific exception handling**: Replacing `except: pass` with specific handlers like `except KeyError` means errors are now logged and reported instead of silently ignored. When debugging production issues, this is invaluable—the difference between knowing "item X wasn't found" versus having no idea why the operation failed.

- **Resource management**: Using context managers with `with open()` ensures files are always closed properly, even when exceptions occur. This prevents resource leaks that could cause "too many open files" errors in long-running applications.

- **Fixed mutable default bug**: The original `logs=[]` would accumulate entries across function calls, causing a subtle bug where logs would mysteriously contain entries from previous operations. This is now impossible.

**Maintainability:**

- **Self-documenting code**: Adding comprehensive docstrings means new developers (or future me!) can understand the code without reading implementation details. The docstrings explain what each function does, what parameters it expects, what it returns, and what exceptions it might raise.

- **Class-based architecture**: Converting from global variables to an `InventoryManager` class makes the code testable. I can now create multiple independent inventory instances, mock them in tests, and ensure operations don't interfere with each other.

- **Consistent naming**: Following Python conventions (snake_case) means the code looks familiar to any Python developer. It's instantly recognizable as professional Python code.

**Readability:**

- **Modern Python idioms**: F-strings like `f"Added {qty} items"` are more readable than old-style formatting `"Added %d items" % qty`. The intent is immediately clear without mentally parsing format codes.

- **Proper spacing**: PEP 8's two-blank-line rule between functions creates visual separation that makes the code structure obvious at a glance. It's easier to scan and find specific functions.

- **Descriptive error messages**: Instead of generic "Error" messages, users now see helpful messages like "Item 'orange' not found in inventory" or "Quantity cannot be negative, got -2". This reduces support burden and improves user experience.

**Measurable Impact:**

The quantitative improvements are striking:
- **Pylint score**: 4.80/10 → 10.00/10 (+109% improvement)
- **Security vulnerabilities**: 2 → 0 (100% reduction)
- **Style violations**: 11 → 0 (100% compliance with PEP 8)
- **Lines of code**: 62 → 255 (but with comprehensive documentation and error handling)

---