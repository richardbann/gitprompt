# gitprompt
A simple `python` script to indicate current `git` branch and status in
`bash` prompt.

## Install
Copy the script (`prompt.py`) into your home directory and put
the following into `.bashrc`:

```bash
set_bash_prompt(){
    PS1="$(python ~/prompt.py)"
}

PROMPT_COMMAND=set_bash_prompt
```

## Disclaimer
The script assumes 256 color terminal, so modification to color codes may be
needed.
Find additional help on terminal coloring: http://misc.flogisoft.com/bash/tip_colors_and_formatting
