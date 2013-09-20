Auto close brackets for Vim
===========================

Huh? There is a ton of such plugins? Another one?

Unfortunately latest Vim (7.4) broke some hacks which allow to keep
undo/repeat sequence.

vial-cramp tries to bring this functionality back without any hacks but
in cost of some transparency.


Features
--------

* closes () {} [] '' ""

* keeps repeat (undo breaked too hard)

* mapping to skip close bracket

* handle <cr>


Installation
------------

vial-cramp is pathogen friendly and only requires vial to be installed::
    
    cd ~/.vim/bundle
    git clone https://github.com/baverman/vial.git
    git clone https://github.com/baverman/vial-cramp.git


Mappings
--------

<Plug>VialCrampLeave
    You must map this to key which leaves insert mode.

    For example::

        imap <esc> <Plug>VialCrampLeave

        " I prefer jk
        imap jk <Plug>VialCrampLeave

<Plug>VialCrampSkip
    Skips closing bracket::

        imap <c-l> <Plug>VialCrampSkip


TODO
----

* configurable list of pairs

* support for multichar brackets

* skip over new lines
