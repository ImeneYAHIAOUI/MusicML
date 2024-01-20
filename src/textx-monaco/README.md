# TeamB Dsl : Monaco Editor 🎵 

Monaco Editor is a versatile code editor that offers a lightweight and feature-rich environment, known for powering Visual Studio Code. In our project, we leverage the capabilities of Monaco Editor to enhance the experience of working with our DSL implemented using TextX through a user-friendly interface for writing, editing, and visualizing code, providing essential features such as syntax highlighting, autocompletion, and error detection related to our DSL.

Check out an example of Monaco Editor in action, highlighting a syntax error in our DSL:
![open](https://github.com/benaissanadim/DSL-MusicML-TeamB/blob/monaco_editor/src/textx-monaco/images/monaco-editor.PNG)

## Usage 

To install the necessary libraries, run the setup.sh script : ```./setup.sh ```
This script verifies the installation status of the `pygls`, `textx` and  `lsprotocol` packages using pip for running the client, and it also checks the installation status of the `yarn` package using npm, installing it if not already present.

### server 
- Run ```./run-server.sh```
### client  
- Run ```./run-client.sh```
- Open in your browser: http://127.0.0.1:4000/


## references :

- Tutorial : [Integrating TextX and Monaco](https://tomassetti.me/integrating-textx-and-monaco-a-non-tutorial/)







