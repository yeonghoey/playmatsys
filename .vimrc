au BufRead,BufNewFile *.kv set syntax=kivy

let @k='matsysskill.py'

"~/.vim/after/compiler/kivy.vim
let g:dispatch_compilers = {'kivy': 'kivy'}
nnoremap <F10> :update %<CR>:Dispatch kivy <C-R>k<CR>
