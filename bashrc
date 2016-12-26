set_bash_prompt(){
    PS1="$(python ~/gitprompt/prompt.py)"
}

PROMPT_COMMAND=set_bash_prompt
