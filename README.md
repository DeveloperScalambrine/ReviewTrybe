# CSS Selectors Summary

CSS selectors are patterns used to select the HTML element(s) you want to style.  They are essential for targeting specific elements and applying styles efficiently.  This document provides a summary of common CSS selectors.

## Basic Selectors

* **Element Selector:** Selects elements based on their tag name.

    ```css
    p {
        color: blue;
    }
    ```

* **ID Selector:** Selects a single element with a specific ID.  IDs should be unique within a document.

    ```css
    #my-paragraph {
        font-weight: bold;
    }
    ```

* **Class Selector:** Selects all elements with a specific class.  Multiple elements can share the same class.

    ```css
    .highlight {
        background-color: yellow;
    }
    ```

* **Universal Selector:** Selects all elements in the document.

    ```css
    * {
        box-sizing: border-box;
    }
    ```

## Combinator Selectors

* **Descendant Combinator (`space`):** Selects all descendants of an element.

    ```css
    div p {
        font-size: 14px;
    }
    ```

* **Child Combinator (`>`):** Selects only direct children of an element.

    ```css
    ul > li {
        list-style-type: square;
    }
    ```

* **Adjacent Sibling Combinator (`+`):** Selects the immediately following sibling of an element.

    ```css
    h2 + p {
        margin-top: 0;
    }
    ```

* **General Sibling Combinator (`~`):** Selects all following siblings of an element.

    ```css
    h2 ~ p {
        font-style: italic;
    }
    ```


## Attribute Selectors

* **`[attribute]`:** Selects elements with a specific attribute.

    ```css
    input[type="text"] {
        border: 1px solid gray;
    }
    ```

* **`[attribute=value]`:** Selects elements with a specific attribute and value.

    ```css
    a[href="https://www.example.com"] {
        color: green;
    }
    ```

* **`[attribute*=value]`:** Selects elements with an attribute value containing a specific substring.

    ```css
    img[src*="logo"] {
        width: 100px;
    }
    ```


## Pseudo-classes and Pseudo-elements

* **Pseudo-classes:** Select elements based on their state (e.g., `:hover`, `:focus`, `:first-child`).

    ```css
    a:hover {
        text-decoration: underline;
    }
    ```

* **Pseudo-elements:** Select specific parts of an element (e.g., `::before`, `::after`, `::first-letter`).

    ```css
    p::first-letter {
        font-size: 2em;
    }
    ```


This summary provides a starting point for understanding CSS selectors.  There are many more selectors and combinations available, allowing for fine-grained control over styling.  Refer to the official CSS documentation for more comprehensive information.