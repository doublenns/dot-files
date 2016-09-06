" Basic options --------------------------------------------------------------
let python_highlight_all = 1    " Enable all Python syntax highlighting
filetype on                     " Determine type of file being edited
filetype plugin on              " Diff vim settings based on filetype
if !exists("g:syntax_on")
    syntax enable               " Enable syntax highlighting
endif


" Tabs and spaces ------------------------------------------------------------
set tabstop=4                   " Set tabs to have 4 spaces
set expandtab                   " Expand tabs into spaces
set shiftwidth=4                " shift line 4 spaces w/ >> & << commands


" Indents and wrapping -------------------------------------------------------
set autoindent                  " Indent when moving to the next line


" Visual ---------------------------------------------------------------------
set number                      " Show line numbers
set ruler                       " Show line position
set cursorline                  " Show visual line under cursor's current line
set showmatch                   " Show matching part of pair for {} [] and ()


" Searching ------------------------------------------------------------------
set ignorecase                  " Case-insensitive search
set smartcase                   " Case-sensitive if query contains uppercase
set incsearch                   " Show first search result as query is typed


" Aliases --------------------------------------------------------------------
command Nonum set nonumber          " Useful when copying and pasting via OS
command Num set number              " Used to undo the above alias
command Noindent set noautoindent   " Useful when copying and pasting via OS
command Indent set autoindent       " Used to undo the above alias

