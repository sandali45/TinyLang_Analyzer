## 🌟 **TinyLang\_Analyzer**

TinyLang\_Analyzer is a lightweight lexical analysis tool designed to process programs written in the simplified programming language **TinyLang**. It acts as the crucial first phase of a compiler, meticulously scanning source code and converting it into a sequence of **tokens**. This structured output is then used for subsequent syntax and semantic analysis.

-----

## ✨ **Features**

TinyLang\_Analyzer is built to provide a robust and educational-friendly tokenization process.

| **Category** | **Description** | **Examples** |
| :--- | :--- | :--- |
| **Keywords** | Reserved words with special meaning in TinyLang. | `if`, `else`, `while`, `print` |
| **Identifiers** | User-defined names for variables, functions, etc. | `count`, `my_variable`, `calculate_sum` |
| **Operators** | Symbols that perform operations. | `+`, `-`, `*`, `/`, `=`, `>`, `<` |
| **Constants** | Fixed values, like numbers and strings. | `5`, `100`, `"hello_world"` |
| **Delimiters & Special Symbols** | Characters used to structure code. | `(`, `)`, `{`, `}`, `;`, `,` |

The analyzer also includes a robust error-handling mechanism to **detect and report lexical errors**, ensuring a clean and accurate token stream.

-----

## ⚙️ **How It Works**

TinyLang\_Analyzer follows a straightforward, three-step process to transform source code into tokens.

1.  **Input**: It accepts TinyLang source code, typically from a file (`.txt`) or directly as an inline string.
2.  **Scanning**: The tool reads the input code character by character, matching each sequence against a predefined set of lexical rules.
3.  **Output**: It generates a structured output of tokens, each with its type and position in the source code, ready for further compilation stages.

-----

## 📂 **Example**

Below is a clear illustration of how the analyzer processes a simple TinyLang program.

### Input

```tinylang
int count = 5;
if (count > 0) {
    print(count);
}
```

### Output

| **Token Value** | **Token Type** |
| :--- | :--- |
| `int` | `keyword` |
| `count` | `identifier` |
| `=` | `operator` |
| `5` | `constant` |
| `;` | `delimiter` |
| `if` | `keyword` |
| `(` | `delimiter` |
| `count` | `identifier` |
| `>` | `operator` |
| `0` | `constant` |
| `)` | `delimiter` |
| `{` | `delimiter` |
| `print` | `identifier` |
| `(` | `delimiter` |
| `count` | `identifier` |
| `)` | `delimiter` |
| `;` | `delimiter` |
| `}` | `delimiter` |

-----

## 🚀 **Use Cases**

TinyLang\_Analyzer is a versatile tool, particularly for academic and educational purposes.

  * **Compiler Construction Projects**: An ideal starting point for building a full-fledged compiler.
  * **Educational Demonstrations**: Visually explains the core concepts of **lexical analysis** and tokenization.
  * **Preprocessing**: Can be used as a front-end for interpreters and other code analysis tools.

This README provides a comprehensive overview of the **TinyLang\_Analyzer**. Ready to get started? Feel free to clone the repository and explore the code\!
