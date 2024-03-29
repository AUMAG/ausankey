# Changelog for ausankey

## 2024-99-99 v1.3

* Add `label_duplicate` switch to avoid printing redundant labels.
* Internal code changes using OOP methods to assist further features. 


## 2024-03-25 v1.2.1

* Label alignment bug fix (not sure how it slipped through).
* Fixing it involved some nice tidy-up of the code. 
* Took the opportunity to flesh out the documentation a little.


## 2024-03-25 v1.2

* Many more configuration options. (E.g., edges around flows/nodes, transparency of nodes, properties of label and title text, alignment of labels, …)
* Now allows flows that start and stop (which work with sorting).
* Reference documentation added to supplement the user documentation.
* Some breaking changes but no-one is using this besides me, right?
 

## 2024-03-14 v1.1

* Change package name from `auSankey` to `ausankey` to match Python standards
* All `mixedCase` options converted to `snake_case`
* Package management updated to `pypackage.toml` and build system now uses `hatch`
* Repository tidied up


## 2024-03-12 v1.0

* Initial release
