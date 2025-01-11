# Changelog for ausankey

## 2025-01-11 v1.6

* Remove redundant `_val` suffix in various `...thresh_val` parameters.
* Change `...thresh_sum` parameters to `...thresh_ofsum` — I kept stumbling over the previous name. Some more parameters of this type added as well.
* Add some `..._thresh_ofmax` parameters which act on the maximum of the node sums for each stage.
* For consistency change the current `...thresh_max` parameters to `...ofmax` and change their logic accordingly — their old definitions seemed of marginal better in practice.


## 2024-12-08 v1.5

* Set xticks and xticklabels in case sankey plot is used with `ax.axis("on")`
* Add additional labelling feature to annotate nodes with their relative percentages. A variety of customisation options.
* Add `value_duplicate = False` to avoid redundant labelling.
* Add `label_thresh` to turn off labels for nodes below a certain size.
* Add `value_fn`, as alternative to `label_format`, which allows more generalised formatting of each value using a lambda function.
* Add values to node labels when `label_values = True`.
* Allow NaN or None when flows terminate.


## 2024-05-29 v1.4

* Fix alignment bug when nodes were changing their
  label and stopping/starting. 
* Fix title alignment bug when second-to-last and
  last stages had different nodes on top.  
* Add `top` option for `label_loc`.
* Start a doc page to collate some examples.
* Substantial code refactoring (which I sometimes
  worry is closer to obfuscation). 
 

## 2024-04-07 v1.3

* Add `value_loc` option to control printing
  of numeric values of flows. Several accompanying
  options control the typesetting, etc.
* Add `label_duplicate` option to avoid printing 
  redundant labels.
* Add `other_thresh_XX` options to allow 
  recategorisation of entries with values below a
  certain threshold.
* Add `sort_dict` option to override sort order for
  individual labels.
* Internal code changes using OOP methods to
  tidy up.


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
