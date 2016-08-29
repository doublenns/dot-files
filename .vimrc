" Enable different vim settings based on the filetype being edited
filetype plugin on

" Enable syntax highlighting
syntax enable

" Show line numbers
set number

" Set tabs to have 4 spaces
set tabstop=4

" Expand tabs into spaces
set expandtab

" Indent when moving to the next line when writing code
set autoindent

" Show visual line under cursor's current line
set cursorline

" When using the >> or << commands, shift lines by 4 spaces
set shiftwidth=4

" Show the matching part of the pair for {} [] and ()
set showmatch

" Enable all Python syntax highlighting features
let python_highlight_all = 1

" Alias ':Nonum' within vim to 'set nonumber' command
" Useful when copying and pasting via OS highlighting across terms
command Nonum set nonumber

" Alias ':Num' within vim to 'set number' command
" Used within workflow of undoing the above alias
command Num set number


" Alias ':Noindent' within vim to 'set noautoindent' command
" Useful when copying and pasting via OS highlighting across terms
command Noindent set noautoindent

" Alias ':Indent' within vim to 'set autoindent' command
" Used within workflow of undoing the above alias
command Indent set autoindent
