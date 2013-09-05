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

* keeps undo/repeat

* mapping to skip close bracket


Mappings
--------

<Plug>VialCrampLeave
    You must map this to key which leaves insert mode.

    For example::

        imap <esc> <Plug>VialCrampLeave

        # I prefer jk
        imap jk <Plug>VialCrampLeave

<Plug>VialCrampSkip
    Skips closing bracket


TODO
----

* support for multichar brackets

* handle BackSpace key
