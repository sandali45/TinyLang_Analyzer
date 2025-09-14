# TinyLang_Analyzer

TinyLang_Analyser is a lightweight lexical analysis tool built to process programs written in the simplified programming language TinyLang. It serves as the first phase of compilation, scanning source code and converting it into a sequence of tokens that can be further used for syntax and semantic analysis.

✨ ##Features

Supports tokenization for:

Keywords (e.g., if, else, while)

Identifiers (variables, function names)

Operators (+, -, *, /, =, etc.)

Constants (numbers, strings)

Delimiters & Special Symbols (;, ,, (, ))

Detects and reports lexical errors.

Produces structured token tables for analysis.

Designed for educational use in compiler design projects.

##⚙️ How It Works

Input: TinyLang source code (e.g., .txt file or inline code).

Scanning: Code is read character by character and matched against lexical rules.

Output: Tokens with their type and position in the source code.

##📂 Example
Input
int count = 5;
if (count > 0) {
    print(count);
}

Output
[int, keyword]  
[count, identifier]  
[=, operator]  
[5, constant]  
[;, delimiter]  
[if, keyword]  
[(, delimiter]  
[count, identifier]  
[>, operator]  
[0, constant]  
[), delimiter]  
[{, delimiter]  
[print, identifier]  
[(, delimiter]  
[count, identifier]  
[), delimiter]  
[;, delimiter]  
[}, delimiter]  

##🚀 Use Cases

Compiler construction projects.

Educational demonstrations of lexical analysis.

Preprocessing for interpreters and analyzers.
