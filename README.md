# gitprompt
A simple `python` script to indicate current `git` branch and status in
`bash` prompt.

## Install
Clone this repo somewhere on your machine:

```bash
cd [somedir]
git clone https://github.com/richardbann/gitprompt.git
```

Now append this code to your `.bashrc`:

```bash
set_bash_prompt(){
    PS1="$(python [somedir]/gitprompt/prompt.py)"
}

PROMPT_COMMAND=set_bash_prompt
```

Be careful to change `somedir` above according to where you have cloned the repo.

## Disclaimer
The script assumes 256 color terminal, so modification to color codes may be
needed.
Find additional help on terminal coloring: http://misc.flogisoft.com/bash/tip_colors_and_formatting

You can see experiment with foreground and background colors by running `256-colors.sh` from the site above.
