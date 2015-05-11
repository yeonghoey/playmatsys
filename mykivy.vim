au BufRead,BufNewFile *.kv set syntax=kivy

let @k='main.py'
set tags+=/Applications/Kivy.app/Contents/Resources/kivy/kivy/tags

"~/.vim/after/compiler/kivy.vim
let g:dispatch_compilers = {'kivy': 'kivy'}

nnoremap <F10> :update %<CR>:Dispatch kivy <C-R>k<CR>
