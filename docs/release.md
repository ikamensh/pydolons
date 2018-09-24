* @date:2018.09.24
@autor:reef425
@note_start:
Закоментировал код в `battlefield/Battlefield.py`
Из за того что
`from game_objects.battlefield_objects*` -- вызываяет импорт `Unit`.
`Battlefield` -- сам вызывается в `Unit` через импорт `from mechanics.events*`
@note_end
