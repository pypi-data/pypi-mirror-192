# MIT License
#
# Copyright (c) 2015-2022 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Union

from selene.core.entity import Element
from selene.core.wait import Command


# noinspection PyPep8Naming
class js:
    @staticmethod
    def set_value(value: Union[str, int]) -> Command[Element]:
        def fn(element: Element):
            element.execute_script(
                """
                var text = arguments[0];
                var maxlength = element.getAttribute('maxlength') === null
                    ? -1
                    : parseInt(element.getAttribute('maxlength'));
                element.value = maxlength === -1
                    ? text
                    : text.length <= maxlength
                        ? text
                        : text.substring(0, maxlength);
                return null;
                """,
                str(value),
            )

        return Command(f'set value by js: {value}', fn)

    @staticmethod
    def type(keys: Union[str, int]) -> Command[Element]:
        def fn(element: Element):
            element.execute_script(
                """
                textToAppend = arguments[0];
                var value = element.value || '';
                var text = value + textToAppend;
                var maxlength = element.getAttribute('maxlength') === null
                    ? -1
                    : parseInt(element.getAttribute('maxlength'));
                element.value = maxlength === -1
                    ? text
                    : text.length <= maxlength
                        ? text
                        : text.substring(0, maxlength);
                return null;
                """,
                str(keys),
            )

        return Command(f'set value by js: {keys}', fn)

    scroll_into_view = Command(
        'scroll into view',
        lambda element: element.execute_script('element.scrollIntoView(true)'),
    )

    click = Command(
        'click',
        lambda element: element.execute_script('element.click()'),
    )

    clear_local_storage = Command(
        'clear local storage',
        lambda browser: browser.driver.execute_script(
            'window.localStorage.clear()'
        ),
    )

    clear_session_storage = Command(
        'clear local storage',
        lambda browser: browser.driver.execute_script(
            'window.sessionStorage.clear()'
        ),
    )

    remove = Command(
        'remove',
        lambda entity: (
            entity.execute_script('element.remove()')
            if not hasattr(entity, '__iter__')
            else [
                element.execute_script('element.remove()')
                for element in entity
            ]
        ),
    )

    @staticmethod
    def set_style_property(
        name: str, value: Union[str, int]
    ) -> Command[Element]:
        return Command(
            f'set element.style.{name}="{value}"',
            lambda entity: (
                entity.execute_script(f'element.style.{name}="{value}"')
                if not hasattr(entity, '__iter__')
                else [
                    element.execute_script(f'element.style.{name}="{value}"')
                    for element in entity
                ]
            ),
        )

    set_style_display_to_none = Command(
        'set element.style.display="none"',
        lambda entity: (
            entity.execute_script('element.style.display="none"')
            if not hasattr(entity, '__iter__')
            else [
                element.execute_script('element.style.display="none"')
                for element in entity
            ]
        ),
    )

    set_style_display_to_block = Command(
        'set element.style.display="block"',
        lambda entity: (
            entity.execute_script('element.style.display="block"')
            if not hasattr(entity, '__iter__')
            else [
                element.execute_script('element.style.display="block"')
                for element in entity
            ]
        ),
    )

    set_style_visibility_to_hidden = Command(
        'set element.style.visibility="hidden"',
        lambda entity: (
            entity.execute_script('element.style.visibility="hidden"')
            if not hasattr(entity, '__iter__')
            else [
                element.execute_script('element.style.visibility="hidden"')
                for element in entity
            ]
        ),
    )

    set_style_visibility_to_visible = Command(
        'set element.style.visibility="visible"',
        lambda entity: (
            entity.execute_script('element.style.visibility="visible"')
            if not hasattr(entity, '__iter__')
            else [
                element.execute_script('element.style.visibility="visible"')
                for element in entity
            ]
        ),
    )
