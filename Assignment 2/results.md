# Experiment results

Training sentences: {'tolkien': 4979, 'doyle': 3934}, dev passages: 329

## Part 0: Typography confound

The Hobbit file uses curly quotes/em-dashes; The Lost World file uses straight quotes and '--'. 'Swapped' re-typesets each dev passage in the OTHER book's style. Config: {'vocab_size': 5000, 'pretokenizer': 'whitespace', 'lowercase': False, 'n': 2, 'k': 0.01}

| training text | dev acc (as-is) | dev acc (typography swapped) |
|---|---|---|
| raw | 0.9851 | 0.8423 |
| normalized | 0.9696 | 0.9696 |

## Part 1: Tokenizer

Tokens/word is measured on the held-out dev text (lower = longer merges).

| pre-tokenizer | requested V | learned V | tokens/word | <unk> on dev |
|---|---|---|---|---|
| whitespace | 500 | 500 | 1.993 | 0 |
| whitespace | 1000 | 1000 | 1.712 | 0 |
| whitespace | 2000 | 2000 | 1.502 | 0 |
| whitespace | 5000 | 5000 | 1.321 | 0 |
| whitespace | 10000 | 9535 | 1.250 | 0 |
| ws_only | 500 | 500 | 1.979 | 0 |
| ws_only | 1000 | 1000 | 1.690 | 0 |
| ws_only | 2000 | 2000 | 1.473 | 0 |
| ws_only | 5000 | 5000 | 1.267 | 0 |
| ws_only | 10000 | 10000 | 1.169 | 0 |
| bytelevel | 500 | 500 | 2.447 | 0 |
| bytelevel | 1000 | 1000 | 1.878 | 0 |
| bytelevel | 2000 | 2000 | 1.580 | 0 |
| bytelevel | 5000 | 5000 | 1.355 | 0 |
| bytelevel | 10000 | 10000 | 1.261 | 0 |

Example segmentations:

- **whitespace, V=500**: `Gandalf ! I f you had he ard only a qu ar ter of what I have he ard about him , and I have only he ard very little of all there`
- **whitespace, V=5000**: `Gandalf ! If you had heard only a quar ter of what I have heard about him , and I have only heard very little of all there`
- **ws_only, V=500**: `Gandalf ! I f you had he ard only a qu ar ter of what I have he ard about him , and I have only he ard very little of all there`
- **ws_only, V=5000**: `Gandalf ! If you had heard only a quar ter of what I have heard about him, and I have only heard very little of all there`
- **bytelevel, V=500**: `ĠG and al f ! ĠI f Ġyou Ġhad Ġhe ard Ġon ly Ġa Ġ qu ar ter Ġof Ġw hat ĠI Ġhave Ġhe ard Ġa b out Ġhim , Ġand ĠI Ġhave Ġon ly Ġhe ard Ġ very Ġl it t le Ġof Ġall Ġthere Ġ`
- **bytelevel, V=5000**: `ĠGandalf ! ĠIf Ġyou Ġhad Ġheard Ġonly Ġa Ġqu ar ter Ġof Ġwhat ĠI Ġhave Ġheard Ġabout Ġhim , Ġand ĠI Ġhave Ġonly Ġheard Ġvery Ġlittle Ġof Ġall Ġthere Ġ`

## Part 2: N-gram perplexity

Shared tokenizer: whitespace, V=5000. Rows are the author the LM was trained on; 'eval on' is held-out text. Perplexity = per-word average negative log probability in nats (assignment definition; lower is better). 'per token' averages over predicted BPE tokens; 'per ws-word' over whitespace words, which is comparable across vocab sizes. exp(.) shown for reference only.


| LM trained on | eval on | n | k | perplexity (per token) | perplexity (per ws-word) | exp(per token) |
|---|---|---|---|---|---|---|
| tolkien | tolkien | 1 | 1.0 | 6.321 | 8.131 | 556.0 |
| tolkien | tolkien | 1 | 0.1 | 6.323 | 8.134 | 557.3 |
| tolkien | tolkien | 1 | 0.01 | 6.332 | 8.146 | 562.4 |
| tolkien | tolkien | 1 | 0.001 | 6.342 | 8.158 | 567.8 |
| tolkien | tolkien | 2 | 1.0 | 6.969 | 8.964 | 1062.9 |
| tolkien | tolkien | 2 | 0.1 | 6.153 | 7.915 | 470.2 |
| tolkien | tolkien | 2 | 0.01 | 5.864 | 7.544 | 352.2 |
| tolkien | tolkien | 2 | 0.001 | 6.145 | 7.905 | 466.5 |
| tolkien | tolkien | 3 | 1.0 | 8.089 | 10.406 | 3258.9 |
| tolkien | tolkien | 3 | 0.1 | 7.615 | 9.796 | 2029.1 |
| tolkien | tolkien | 3 | 0.01 | 7.231 | 9.302 | 1382.1 |
| tolkien | tolkien | 3 | 0.001 | 7.219 | 9.286 | 1365.2 |
| tolkien | doyle | 1 | 1.0 | 6.881 | 9.692 | 973.6 |
| tolkien | doyle | 1 | 0.1 | 6.996 | 9.854 | 1091.8 |
| tolkien | doyle | 1 | 0.01 | 7.098 | 9.998 | 1209.8 |
| tolkien | doyle | 1 | 0.001 | 7.199 | 10.140 | 1337.6 |
| tolkien | doyle | 2 | 1.0 | 7.452 | 10.497 | 1724.1 |
| tolkien | doyle | 2 | 0.1 | 6.967 | 9.814 | 1061.3 |
| tolkien | doyle | 2 | 0.01 | 6.956 | 9.798 | 1049.3 |
| tolkien | doyle | 2 | 0.001 | 7.483 | 10.541 | 1778.0 |
| tolkien | doyle | 3 | 1.0 | 8.290 | 11.678 | 3985.6 |
| tolkien | doyle | 3 | 0.1 | 8.076 | 11.376 | 3216.5 |
| tolkien | doyle | 3 | 0.01 | 7.942 | 11.187 | 2814.2 |
| tolkien | doyle | 3 | 0.001 | 8.067 | 11.363 | 3188.6 |

| LM trained on | eval on | n | k | perplexity (per token) | perplexity (per ws-word) | exp(per token) |
|---|---|---|---|---|---|---|
| doyle | tolkien | 1 | 1.0 | 6.648 | 8.551 | 771.0 |
| doyle | tolkien | 1 | 0.1 | 6.754 | 8.688 | 857.3 |
| doyle | tolkien | 1 | 0.01 | 6.860 | 8.825 | 953.5 |
| doyle | tolkien | 1 | 0.001 | 6.966 | 8.961 | 1059.8 |
| doyle | tolkien | 2 | 1.0 | 7.379 | 9.492 | 1601.4 |
| doyle | tolkien | 2 | 0.1 | 6.824 | 8.778 | 919.3 |
| doyle | tolkien | 2 | 0.01 | 6.771 | 8.710 | 872.3 |
| doyle | tolkien | 2 | 0.001 | 7.268 | 9.349 | 1433.5 |
| doyle | tolkien | 3 | 1.0 | 8.294 | 10.669 | 3999.0 |
| doyle | tolkien | 3 | 0.1 | 8.068 | 10.379 | 3191.4 |
| doyle | tolkien | 3 | 0.01 | 7.926 | 10.195 | 2767.6 |
| doyle | tolkien | 3 | 0.001 | 8.055 | 10.361 | 3148.8 |
| doyle | doyle | 1 | 1.0 | 6.577 | 9.264 | 718.2 |
| doyle | doyle | 1 | 0.1 | 6.584 | 9.274 | 723.7 |
| doyle | doyle | 1 | 0.01 | 6.596 | 9.291 | 732.5 |
| doyle | doyle | 1 | 0.001 | 6.609 | 9.309 | 741.5 |
| doyle | doyle | 2 | 1.0 | 7.217 | 10.166 | 1362.8 |
| doyle | doyle | 2 | 0.1 | 6.436 | 9.065 | 623.6 |
| doyle | doyle | 2 | 0.01 | 6.133 | 8.638 | 460.6 |
| doyle | doyle | 2 | 0.001 | 6.429 | 9.056 | 619.9 |
| doyle | doyle | 3 | 1.0 | 8.176 | 11.516 | 3553.6 |
| doyle | doyle | 3 | 0.1 | 7.783 | 10.962 | 2398.9 |
| doyle | doyle | 3 | 0.01 | 7.455 | 10.501 | 1728.5 |
| doyle | doyle | 3 | 0.001 | 7.445 | 10.487 | 1711.6 |

## Part 3: Author identification (dev accuracy)

Passages = consecutive sentences held out from each book.

Top 10 configs by accuracy averaged over passage lengths:

| pre-tok | lower | V | n | k | acc 3-sent | acc 1-sent | mean |
|---|---|---|---|---|---|---|---|
| whitespace | True | 10000 | 1 | 1.0 | 0.9848 | 0.9090 | 0.9469 |
| whitespace | True | 10000 | 1 | 0.1 | 0.9818 | 0.9090 | 0.9454 |
| bytelevel | False | 10000 | 1 | 0.1 | 0.9878 | 0.9009 | 0.9444 |
| whitespace | False | 10000 | 1 | 0.1 | 0.9848 | 0.9029 | 0.9439 |
| whitespace | False | 10000 | 1 | 1.0 | 0.9787 | 0.9090 | 0.9439 |
| bytelevel | False | 5000 | 1 | 0.1 | 0.9848 | 0.9009 | 0.9429 |
| bytelevel | False | 10000 | 1 | 1.0 | 0.9818 | 0.9039 | 0.9429 |
| whitespace | True | 2000 | 2 | 1.0 | 0.9757 | 0.9100 | 0.9428 |
| whitespace | True | 10000 | 1 | 0.01 | 0.9757 | 0.9090 | 0.9423 |
| bytelevel | False | 5000 | 1 | 0.01 | 0.9848 | 0.8979 | 0.9413 |

Chosen: {'pretokenizer': 'whitespace', 'lowercase': True, 'vocab_size': 10000, 'n': 1, 'k': 1.0} (mean acc 0.9469)

Full grid:

| sents/passage | pre-tok | lower | V | n | k | accuracy |
|---|---|---|---|---|---|---|
| 3 | bytelevel | False | 10000 | 1 | 0.1 | 0.9878 |
| 3 | whitespace | False | 10000 | 1 | 0.1 | 0.9848 |
| 3 | whitespace | True | 10000 | 1 | 1.0 | 0.9848 |
| 3 | ws_only | False | 5000 | 1 | 0.1 | 0.9848 |
| 3 | ws_only | False | 5000 | 1 | 0.01 | 0.9848 |
| 3 | ws_only | False | 5000 | 1 | 0.001 | 0.9848 |
| 3 | bytelevel | False | 5000 | 1 | 0.1 | 0.9848 |
| 3 | bytelevel | False | 5000 | 1 | 0.01 | 0.9848 |
| 3 | whitespace | True | 10000 | 1 | 0.1 | 0.9818 |
| 3 | ws_only | False | 5000 | 1 | 1.0 | 0.9818 |
| 3 | ws_only | False | 10000 | 1 | 1.0 | 0.9818 |
| 3 | bytelevel | False | 2000 | 2 | 0.1 | 0.9818 |
| 3 | bytelevel | False | 5000 | 1 | 0.001 | 0.9818 |
| 3 | bytelevel | False | 10000 | 1 | 1.0 | 0.9818 |
| 3 | bytelevel | False | 10000 | 1 | 0.01 | 0.9818 |
| 3 | bytelevel | False | 10000 | 1 | 0.001 | 0.9818 |
| 3 | whitespace | False | 5000 | 1 | 0.1 | 0.9787 |
| 3 | whitespace | False | 5000 | 1 | 0.01 | 0.9787 |
| 3 | whitespace | False | 10000 | 1 | 1.0 | 0.9787 |
| 3 | whitespace | True | 2000 | 2 | 0.1 | 0.9787 |
| 3 | whitespace | True | 2000 | 2 | 0.01 | 0.9787 |
| 3 | whitespace | True | 5000 | 1 | 0.1 | 0.9787 |
| 3 | whitespace | True | 5000 | 2 | 0.01 | 0.9787 |
| 3 | ws_only | False | 10000 | 1 | 0.1 | 0.9787 |
| 3 | bytelevel | False | 500 | 2 | 0.01 | 0.9787 |
| 3 | bytelevel | False | 500 | 3 | 0.01 | 0.9787 |
| 3 | bytelevel | False | 2000 | 2 | 0.01 | 0.9787 |
| 3 | bytelevel | False | 2000 | 2 | 0.001 | 0.9787 |
| 3 | whitespace | False | 1000 | 2 | 0.1 | 0.9757 |
| 3 | whitespace | False | 2000 | 2 | 0.1 | 0.9757 |
| 3 | whitespace | False | 2000 | 2 | 0.01 | 0.9757 |
| 3 | whitespace | False | 5000 | 1 | 0.001 | 0.9757 |
| 3 | whitespace | False | 10000 | 1 | 0.01 | 0.9757 |
| 3 | whitespace | False | 10000 | 1 | 0.001 | 0.9757 |
| 3 | whitespace | True | 1000 | 2 | 0.1 | 0.9757 |
| 3 | whitespace | True | 1000 | 3 | 0.1 | 0.9757 |
| 3 | whitespace | True | 2000 | 2 | 1.0 | 0.9757 |
| 3 | whitespace | True | 5000 | 1 | 1.0 | 0.9757 |
| 3 | whitespace | True | 5000 | 1 | 0.01 | 0.9757 |
| 3 | whitespace | True | 5000 | 2 | 0.1 | 0.9757 |
| 3 | whitespace | True | 10000 | 1 | 0.01 | 0.9757 |
| 3 | ws_only | False | 500 | 2 | 0.1 | 0.9757 |
| 3 | bytelevel | False | 500 | 2 | 0.1 | 0.9757 |
| 3 | bytelevel | False | 500 | 3 | 0.1 | 0.9757 |
| 3 | bytelevel | False | 500 | 3 | 0.001 | 0.9757 |
| 3 | bytelevel | False | 1000 | 2 | 0.1 | 0.9757 |
| 3 | bytelevel | False | 1000 | 2 | 0.01 | 0.9757 |
| 3 | bytelevel | False | 1000 | 3 | 1.0 | 0.9757 |
| 3 | bytelevel | False | 5000 | 1 | 1.0 | 0.9757 |
| 3 | whitespace | False | 500 | 2 | 0.1 | 0.9726 |
| 3 | whitespace | False | 2000 | 1 | 1.0 | 0.9726 |
| 3 | whitespace | False | 2000 | 1 | 0.1 | 0.9726 |
| 3 | whitespace | False | 2000 | 1 | 0.01 | 0.9726 |
| 3 | whitespace | False | 2000 | 1 | 0.001 | 0.9726 |
| 3 | whitespace | False | 2000 | 2 | 0.001 | 0.9726 |
| 3 | whitespace | True | 500 | 3 | 0.1 | 0.9726 |
| 3 | whitespace | True | 5000 | 1 | 0.001 | 0.9726 |
| 3 | ws_only | False | 2000 | 2 | 0.1 | 0.9726 |
| 3 | ws_only | False | 10000 | 1 | 0.01 | 0.9726 |
| 3 | bytelevel | False | 500 | 2 | 0.001 | 0.9726 |
| 3 | bytelevel | False | 1000 | 3 | 0.1 | 0.9726 |
| 3 | bytelevel | False | 2000 | 2 | 1.0 | 0.9726 |
| 3 | bytelevel | False | 2000 | 3 | 1.0 | 0.9726 |
| 3 | bytelevel | False | 5000 | 2 | 0.1 | 0.9726 |
| 3 | whitespace | False | 500 | 2 | 0.01 | 0.9696 |
| 3 | whitespace | False | 500 | 2 | 0.001 | 0.9696 |
| 3 | whitespace | False | 500 | 3 | 0.01 | 0.9696 |
| 3 | whitespace | False | 1000 | 2 | 1.0 | 0.9696 |
| 3 | whitespace | False | 1000 | 2 | 0.01 | 0.9696 |
| 3 | whitespace | False | 1000 | 2 | 0.001 | 0.9696 |
| 3 | whitespace | False | 1000 | 3 | 0.1 | 0.9696 |
| 3 | whitespace | False | 5000 | 1 | 1.0 | 0.9696 |
| 3 | whitespace | False | 5000 | 2 | 0.1 | 0.9696 |
| 3 | whitespace | False | 5000 | 2 | 0.01 | 0.9696 |
| 3 | whitespace | True | 500 | 2 | 0.1 | 0.9696 |
| 3 | whitespace | True | 500 | 3 | 1.0 | 0.9696 |
| 3 | whitespace | True | 1000 | 2 | 1.0 | 0.9696 |
| 3 | whitespace | True | 1000 | 2 | 0.01 | 0.9696 |
| 3 | whitespace | True | 1000 | 3 | 1.0 | 0.9696 |
| 3 | whitespace | True | 2000 | 1 | 1.0 | 0.9696 |
| 3 | whitespace | True | 2000 | 1 | 0.1 | 0.9696 |
| 3 | whitespace | True | 2000 | 2 | 0.001 | 0.9696 |
| 3 | whitespace | True | 10000 | 1 | 0.001 | 0.9696 |
| 3 | whitespace | True | 10000 | 2 | 0.01 | 0.9696 |
| 3 | ws_only | False | 500 | 2 | 1.0 | 0.9696 |
| 3 | ws_only | False | 500 | 3 | 0.01 | 0.9696 |
| 3 | ws_only | False | 2000 | 1 | 0.1 | 0.9696 |
| 3 | ws_only | False | 2000 | 1 | 0.01 | 0.9696 |
| 3 | ws_only | False | 2000 | 1 | 0.001 | 0.9696 |
| 3 | ws_only | False | 5000 | 2 | 0.1 | 0.9696 |
| 3 | ws_only | False | 10000 | 1 | 0.001 | 0.9696 |
| 3 | bytelevel | False | 1000 | 2 | 1.0 | 0.9696 |
| 3 | bytelevel | False | 1000 | 2 | 0.001 | 0.9696 |
| 3 | bytelevel | False | 1000 | 3 | 0.01 | 0.9696 |
| 3 | bytelevel | False | 2000 | 3 | 0.1 | 0.9696 |
| 3 | whitespace | False | 500 | 3 | 0.1 | 0.9666 |
| 3 | whitespace | False | 2000 | 2 | 1.0 | 0.9666 |
| 3 | whitespace | True | 500 | 2 | 0.01 | 0.9666 |
| 3 | whitespace | True | 500 | 2 | 0.001 | 0.9666 |
| 3 | whitespace | True | 2000 | 3 | 1.0 | 0.9666 |
| 3 | whitespace | True | 5000 | 2 | 0.001 | 0.9666 |
| 3 | ws_only | False | 500 | 2 | 0.01 | 0.9666 |
| 3 | ws_only | False | 500 | 3 | 0.1 | 0.9666 |
| 3 | ws_only | False | 1000 | 2 | 1.0 | 0.9666 |
| 3 | ws_only | False | 1000 | 2 | 0.1 | 0.9666 |
| 3 | ws_only | False | 1000 | 3 | 1.0 | 0.9666 |
| 3 | ws_only | False | 1000 | 3 | 0.1 | 0.9666 |
| 3 | ws_only | False | 2000 | 2 | 1.0 | 0.9666 |
| 3 | ws_only | False | 2000 | 2 | 0.01 | 0.9666 |
| 3 | bytelevel | False | 10000 | 2 | 0.1 | 0.9666 |
| 3 | bytelevel | False | 10000 | 2 | 0.01 | 0.9666 |
| 3 | whitespace | False | 500 | 2 | 1.0 | 0.9635 |
| 3 | whitespace | False | 1000 | 3 | 1.0 | 0.9635 |
| 3 | whitespace | False | 1000 | 3 | 0.01 | 0.9635 |
| 3 | whitespace | True | 500 | 2 | 1.0 | 0.9635 |
| 3 | whitespace | True | 1000 | 2 | 0.001 | 0.9635 |
| 3 | whitespace | True | 1000 | 3 | 0.01 | 0.9635 |
| 3 | whitespace | True | 2000 | 1 | 0.01 | 0.9635 |
| 3 | whitespace | True | 2000 | 3 | 0.1 | 0.9635 |
| 3 | whitespace | True | 2000 | 3 | 0.01 | 0.9635 |
| 3 | whitespace | True | 10000 | 2 | 0.001 | 0.9635 |
| 3 | ws_only | False | 500 | 2 | 0.001 | 0.9635 |
| 3 | ws_only | False | 500 | 3 | 0.001 | 0.9635 |
| 3 | ws_only | False | 2000 | 1 | 1.0 | 0.9635 |
| 3 | ws_only | False | 2000 | 3 | 0.1 | 0.9635 |
| 3 | ws_only | False | 5000 | 2 | 0.01 | 0.9635 |
| 3 | bytelevel | False | 500 | 3 | 1.0 | 0.9635 |
| 3 | bytelevel | False | 2000 | 1 | 1.0 | 0.9635 |
| 3 | bytelevel | False | 2000 | 1 | 0.1 | 0.9635 |
| 3 | bytelevel | False | 2000 | 1 | 0.01 | 0.9635 |
| 3 | bytelevel | False | 2000 | 1 | 0.001 | 0.9635 |
| 3 | bytelevel | False | 5000 | 2 | 1.0 | 0.9635 |
| 3 | bytelevel | False | 5000 | 2 | 0.01 | 0.9635 |
| 3 | bytelevel | False | 5000 | 2 | 0.001 | 0.9635 |
| 3 | whitespace | False | 500 | 3 | 0.001 | 0.9605 |
| 3 | whitespace | False | 10000 | 2 | 0.1 | 0.9605 |
| 3 | whitespace | True | 1000 | 3 | 0.001 | 0.9605 |
| 3 | whitespace | True | 2000 | 1 | 0.001 | 0.9605 |
| 3 | whitespace | True | 5000 | 2 | 1.0 | 0.9605 |
| 3 | whitespace | True | 10000 | 2 | 0.1 | 0.9605 |
| 3 | ws_only | False | 1000 | 3 | 0.01 | 0.9605 |
| 3 | ws_only | False | 2000 | 2 | 0.001 | 0.9605 |
| 3 | ws_only | False | 5000 | 2 | 0.001 | 0.9605 |
| 3 | bytelevel | False | 2000 | 3 | 0.01 | 0.9605 |
| 3 | whitespace | False | 2000 | 3 | 1.0 | 0.9574 |
| 3 | whitespace | False | 5000 | 2 | 1.0 | 0.9574 |
| 3 | whitespace | True | 500 | 3 | 0.01 | 0.9574 |
| 3 | ws_only | False | 500 | 3 | 1.0 | 0.9574 |
| 3 | ws_only | False | 2000 | 3 | 1.0 | 0.9574 |
| 3 | ws_only | False | 2000 | 3 | 0.01 | 0.9574 |
| 3 | bytelevel | False | 500 | 2 | 1.0 | 0.9574 |
| 3 | bytelevel | False | 5000 | 3 | 0.1 | 0.9574 |
| 3 | bytelevel | False | 5000 | 3 | 0.01 | 0.9574 |
| 3 | whitespace | False | 500 | 3 | 1.0 | 0.9544 |
| 3 | whitespace | False | 2000 | 3 | 0.1 | 0.9544 |
| 3 | whitespace | False | 2000 | 3 | 0.001 | 0.9544 |
| 3 | whitespace | False | 5000 | 2 | 0.001 | 0.9544 |
| 3 | whitespace | False | 10000 | 2 | 0.01 | 0.9544 |
| 3 | ws_only | False | 1000 | 2 | 0.01 | 0.9544 |
| 3 | ws_only | False | 1000 | 2 | 0.001 | 0.9544 |
| 3 | whitespace | False | 2000 | 3 | 0.01 | 0.9514 |
| 3 | whitespace | False | 10000 | 2 | 0.001 | 0.9514 |
| 3 | whitespace | True | 500 | 3 | 0.001 | 0.9514 |
| 3 | whitespace | True | 5000 | 3 | 0.1 | 0.9514 |
| 3 | ws_only | False | 1000 | 1 | 0.01 | 0.9514 |
| 3 | ws_only | False | 1000 | 1 | 0.001 | 0.9514 |
| 3 | bytelevel | False | 1000 | 3 | 0.001 | 0.9514 |
| 3 | bytelevel | False | 2000 | 3 | 0.001 | 0.9514 |
| 3 | whitespace | False | 1000 | 1 | 0.1 | 0.9483 |
| 3 | whitespace | False | 1000 | 1 | 0.01 | 0.9483 |
| 3 | whitespace | False | 1000 | 1 | 0.001 | 0.9483 |
| 3 | ws_only | False | 1000 | 1 | 0.1 | 0.9483 |
| 3 | ws_only | False | 5000 | 2 | 1.0 | 0.9483 |
| 3 | ws_only | False | 10000 | 2 | 0.01 | 0.9483 |
| 3 | bytelevel | False | 1000 | 1 | 0.1 | 0.9483 |
| 3 | bytelevel | False | 1000 | 1 | 0.01 | 0.9483 |
| 3 | bytelevel | False | 1000 | 1 | 0.001 | 0.9483 |
| 3 | bytelevel | False | 5000 | 3 | 0.001 | 0.9483 |
| 3 | whitespace | False | 1000 | 3 | 0.001 | 0.9453 |
| 3 | whitespace | False | 5000 | 3 | 1.0 | 0.9453 |
| 3 | whitespace | True | 2000 | 3 | 0.001 | 0.9453 |
| 3 | whitespace | True | 5000 | 3 | 0.01 | 0.9453 |
| 3 | whitespace | True | 10000 | 2 | 1.0 | 0.9453 |
| 3 | ws_only | False | 1000 | 1 | 1.0 | 0.9453 |
| 3 | ws_only | False | 5000 | 3 | 0.1 | 0.9453 |
| 3 | ws_only | False | 10000 | 2 | 0.1 | 0.9453 |
| 3 | bytelevel | False | 5000 | 3 | 1.0 | 0.9453 |
| 3 | bytelevel | False | 10000 | 2 | 1.0 | 0.9453 |
| 3 | bytelevel | False | 10000 | 2 | 0.001 | 0.9453 |
| 3 | bytelevel | False | 10000 | 3 | 0.01 | 0.9453 |
| 3 | whitespace | False | 1000 | 1 | 1.0 | 0.9422 |
| 3 | whitespace | False | 5000 | 3 | 0.1 | 0.9422 |
| 3 | whitespace | False | 5000 | 3 | 0.01 | 0.9422 |
| 3 | whitespace | False | 5000 | 3 | 0.001 | 0.9422 |
| 3 | whitespace | False | 10000 | 3 | 0.01 | 0.9422 |
| 3 | whitespace | True | 5000 | 3 | 1.0 | 0.9422 |
| 3 | ws_only | False | 1000 | 3 | 0.001 | 0.9422 |
| 3 | bytelevel | False | 10000 | 3 | 0.001 | 0.9422 |
| 3 | whitespace | False | 10000 | 3 | 0.1 | 0.9392 |
| 3 | whitespace | False | 10000 | 3 | 0.001 | 0.9392 |
| 3 | whitespace | True | 5000 | 3 | 0.001 | 0.9392 |
| 3 | ws_only | False | 5000 | 3 | 0.01 | 0.9392 |
| 3 | bytelevel | False | 1000 | 1 | 1.0 | 0.9392 |
| 3 | whitespace | False | 10000 | 2 | 1.0 | 0.9362 |
| 3 | whitespace | True | 10000 | 3 | 0.01 | 0.9362 |
| 3 | ws_only | False | 2000 | 3 | 0.001 | 0.9362 |
| 3 | bytelevel | False | 10000 | 3 | 0.1 | 0.9362 |
| 3 | whitespace | True | 1000 | 1 | 0.1 | 0.9331 |
| 3 | whitespace | True | 1000 | 1 | 0.01 | 0.9331 |
| 3 | whitespace | True | 1000 | 1 | 0.001 | 0.9331 |
| 3 | ws_only | False | 10000 | 2 | 1.0 | 0.9331 |
| 3 | ws_only | False | 10000 | 2 | 0.001 | 0.9331 |
| 3 | whitespace | True | 1000 | 1 | 1.0 | 0.9301 |
| 3 | whitespace | True | 10000 | 3 | 0.1 | 0.9301 |
| 3 | whitespace | False | 10000 | 3 | 1.0 | 0.9271 |
| 3 | whitespace | True | 10000 | 3 | 0.001 | 0.9271 |
| 3 | whitespace | True | 500 | 1 | 0.01 | 0.9240 |
| 3 | whitespace | True | 500 | 1 | 0.001 | 0.9240 |
| 3 | whitespace | False | 500 | 1 | 0.001 | 0.9210 |
| 3 | whitespace | True | 500 | 1 | 1.0 | 0.9210 |
| 3 | whitespace | True | 500 | 1 | 0.1 | 0.9210 |
| 3 | whitespace | True | 10000 | 3 | 1.0 | 0.9210 |
| 3 | ws_only | False | 500 | 1 | 0.001 | 0.9210 |
| 3 | ws_only | False | 5000 | 3 | 1.0 | 0.9210 |
| 3 | bytelevel | False | 10000 | 3 | 1.0 | 0.9210 |
| 3 | whitespace | False | 500 | 1 | 1.0 | 0.9179 |
| 3 | whitespace | False | 500 | 1 | 0.1 | 0.9179 |
| 3 | whitespace | False | 500 | 1 | 0.01 | 0.9179 |
| 3 | ws_only | False | 500 | 1 | 1.0 | 0.9179 |
| 3 | ws_only | False | 500 | 1 | 0.1 | 0.9179 |
| 3 | ws_only | False | 500 | 1 | 0.01 | 0.9179 |
| 3 | ws_only | False | 10000 | 3 | 0.1 | 0.9179 |
| 3 | bytelevel | False | 500 | 1 | 0.1 | 0.9179 |
| 3 | bytelevel | False | 500 | 1 | 0.01 | 0.9179 |
| 3 | bytelevel | False | 500 | 1 | 0.001 | 0.9179 |
| 3 | ws_only | False | 5000 | 3 | 0.001 | 0.9149 |
| 3 | bytelevel | False | 500 | 1 | 1.0 | 0.9149 |
| 3 | ws_only | False | 10000 | 3 | 0.01 | 0.9119 |
| 3 | ws_only | False | 10000 | 3 | 1.0 | 0.9027 |
| 3 | ws_only | False | 10000 | 3 | 0.001 | 0.8906 |
| 1 | whitespace | True | 2000 | 2 | 1.0 | 0.9100 |
| 1 | whitespace | False | 10000 | 1 | 1.0 | 0.9090 |
| 1 | whitespace | True | 10000 | 1 | 1.0 | 0.9090 |
| 1 | whitespace | True | 10000 | 1 | 0.1 | 0.9090 |
| 1 | whitespace | True | 10000 | 1 | 0.01 | 0.9090 |
| 1 | whitespace | True | 500 | 3 | 1.0 | 0.9080 |
| 1 | whitespace | True | 10000 | 1 | 0.001 | 0.9070 |
| 1 | bytelevel | False | 1000 | 2 | 1.0 | 0.9050 |
| 1 | whitespace | False | 2000 | 2 | 1.0 | 0.9039 |
| 1 | bytelevel | False | 10000 | 1 | 1.0 | 0.9039 |
| 1 | whitespace | False | 10000 | 1 | 0.1 | 0.9029 |
| 1 | whitespace | True | 5000 | 1 | 1.0 | 0.9029 |
| 1 | whitespace | True | 5000 | 1 | 0.1 | 0.9029 |
| 1 | ws_only | False | 1000 | 2 | 0.1 | 0.9029 |
| 1 | ws_only | False | 5000 | 2 | 0.1 | 0.9029 |
| 1 | bytelevel | False | 500 | 3 | 1.0 | 0.9029 |
| 1 | whitespace | False | 500 | 3 | 0.1 | 0.9019 |
| 1 | whitespace | False | 2000 | 2 | 0.1 | 0.9019 |
| 1 | whitespace | True | 5000 | 1 | 0.01 | 0.9019 |
| 1 | ws_only | False | 2000 | 2 | 1.0 | 0.9019 |
| 1 | whitespace | False | 500 | 3 | 1.0 | 0.9009 |
| 1 | whitespace | True | 500 | 2 | 1.0 | 0.9009 |
| 1 | bytelevel | False | 5000 | 1 | 0.1 | 0.9009 |
| 1 | bytelevel | False | 10000 | 1 | 0.1 | 0.9009 |
| 1 | whitespace | False | 1000 | 2 | 0.1 | 0.8999 |
| 1 | whitespace | True | 500 | 3 | 0.1 | 0.8999 |
| 1 | whitespace | True | 1000 | 2 | 1.0 | 0.8999 |
| 1 | ws_only | False | 5000 | 2 | 1.0 | 0.8999 |
| 1 | bytelevel | False | 2000 | 2 | 1.0 | 0.8999 |
| 1 | whitespace | True | 5000 | 1 | 0.001 | 0.8989 |
| 1 | ws_only | False | 500 | 3 | 1.0 | 0.8989 |
| 1 | bytelevel | False | 1000 | 2 | 0.1 | 0.8989 |
| 1 | bytelevel | False | 5000 | 1 | 1.0 | 0.8989 |
| 1 | whitespace | True | 1000 | 2 | 0.1 | 0.8979 |
| 1 | whitespace | True | 2000 | 2 | 0.1 | 0.8979 |
| 1 | ws_only | False | 1000 | 2 | 1.0 | 0.8979 |
| 1 | bytelevel | False | 5000 | 1 | 0.01 | 0.8979 |
| 1 | bytelevel | False | 5000 | 1 | 0.001 | 0.8979 |
| 1 | whitespace | False | 10000 | 1 | 0.01 | 0.8969 |
| 1 | ws_only | False | 10000 | 1 | 0.1 | 0.8969 |
| 1 | bytelevel | False | 500 | 3 | 0.1 | 0.8969 |
| 1 | bytelevel | False | 2000 | 2 | 0.1 | 0.8969 |
| 1 | whitespace | False | 2000 | 2 | 0.01 | 0.8959 |
| 1 | whitespace | False | 5000 | 1 | 1.0 | 0.8959 |
| 1 | whitespace | False | 5000 | 1 | 0.1 | 0.8959 |
| 1 | whitespace | False | 5000 | 1 | 0.01 | 0.8959 |
| 1 | whitespace | False | 10000 | 1 | 0.001 | 0.8959 |
| 1 | whitespace | True | 500 | 2 | 0.1 | 0.8959 |
| 1 | ws_only | False | 10000 | 1 | 0.01 | 0.8959 |
| 1 | whitespace | False | 1000 | 2 | 1.0 | 0.8948 |
| 1 | whitespace | False | 5000 | 1 | 0.001 | 0.8948 |
| 1 | whitespace | True | 5000 | 2 | 0.1 | 0.8948 |
| 1 | bytelevel | False | 1000 | 3 | 1.0 | 0.8948 |
| 1 | bytelevel | False | 10000 | 1 | 0.001 | 0.8948 |
| 1 | whitespace | False | 500 | 2 | 1.0 | 0.8938 |
| 1 | whitespace | False | 5000 | 2 | 0.1 | 0.8938 |
| 1 | ws_only | False | 2000 | 2 | 0.1 | 0.8938 |
| 1 | bytelevel | False | 1000 | 3 | 0.1 | 0.8938 |
| 1 | bytelevel | False | 10000 | 1 | 0.01 | 0.8938 |
| 1 | ws_only | False | 500 | 2 | 1.0 | 0.8928 |
| 1 | ws_only | False | 500 | 3 | 0.1 | 0.8928 |
| 1 | ws_only | False | 10000 | 1 | 0.001 | 0.8928 |
| 1 | whitespace | True | 5000 | 2 | 0.01 | 0.8918 |
| 1 | ws_only | False | 5000 | 1 | 0.01 | 0.8918 |
| 1 | ws_only | False | 5000 | 1 | 0.001 | 0.8918 |
| 1 | bytelevel | False | 5000 | 2 | 0.1 | 0.8918 |
| 1 | whitespace | False | 500 | 2 | 0.1 | 0.8908 |
| 1 | whitespace | False | 1000 | 3 | 1.0 | 0.8908 |
| 1 | whitespace | True | 10000 | 2 | 0.01 | 0.8908 |
| 1 | ws_only | False | 5000 | 1 | 0.1 | 0.8908 |
| 1 | bytelevel | False | 5000 | 2 | 1.0 | 0.8908 |
| 1 | whitespace | True | 5000 | 2 | 1.0 | 0.8898 |
| 1 | ws_only | False | 500 | 2 | 0.1 | 0.8898 |
| 1 | ws_only | False | 1000 | 2 | 0.01 | 0.8898 |
| 1 | ws_only | False | 5000 | 2 | 0.01 | 0.8888 |
| 1 | ws_only | False | 10000 | 1 | 1.0 | 0.8888 |
| 1 | whitespace | True | 2000 | 2 | 0.01 | 0.8878 |
| 1 | ws_only | False | 1000 | 3 | 1.0 | 0.8878 |
| 1 | whitespace | False | 1000 | 3 | 0.1 | 0.8868 |
| 1 | whitespace | False | 5000 | 2 | 1.0 | 0.8868 |
| 1 | whitespace | True | 10000 | 2 | 0.1 | 0.8868 |
| 1 | whitespace | False | 500 | 3 | 0.01 | 0.8857 |
| 1 | whitespace | True | 1000 | 3 | 1.0 | 0.8857 |
| 1 | whitespace | True | 2000 | 1 | 1.0 | 0.8857 |
| 1 | whitespace | True | 2000 | 1 | 0.1 | 0.8857 |
| 1 | whitespace | True | 2000 | 1 | 0.01 | 0.8857 |
| 1 | whitespace | True | 2000 | 1 | 0.001 | 0.8857 |
| 1 | ws_only | False | 500 | 3 | 0.01 | 0.8857 |
| 1 | whitespace | False | 5000 | 2 | 0.01 | 0.8847 |
| 1 | whitespace | False | 10000 | 2 | 0.1 | 0.8847 |
| 1 | bytelevel | False | 500 | 2 | 1.0 | 0.8847 |
| 1 | whitespace | False | 1000 | 2 | 0.01 | 0.8837 |
| 1 | whitespace | False | 10000 | 2 | 0.01 | 0.8837 |
| 1 | ws_only | False | 2000 | 1 | 0.1 | 0.8837 |
| 1 | ws_only | False | 2000 | 1 | 0.01 | 0.8837 |
| 1 | ws_only | False | 10000 | 2 | 0.1 | 0.8837 |
| 1 | bytelevel | False | 500 | 3 | 0.01 | 0.8837 |
| 1 | bytelevel | False | 5000 | 2 | 0.01 | 0.8837 |
| 1 | whitespace | True | 1000 | 2 | 0.01 | 0.8827 |
| 1 | ws_only | False | 1000 | 3 | 0.1 | 0.8827 |
| 1 | ws_only | False | 2000 | 1 | 0.001 | 0.8827 |
| 1 | whitespace | False | 2000 | 1 | 0.1 | 0.8817 |
| 1 | whitespace | False | 2000 | 1 | 0.01 | 0.8817 |
| 1 | whitespace | False | 2000 | 1 | 0.001 | 0.8817 |
| 1 | whitespace | True | 500 | 2 | 0.01 | 0.8817 |
| 1 | whitespace | True | 2000 | 2 | 0.001 | 0.8817 |
| 1 | ws_only | False | 2000 | 2 | 0.01 | 0.8817 |
| 1 | ws_only | False | 5000 | 1 | 1.0 | 0.8817 |
| 1 | bytelevel | False | 10000 | 2 | 0.1 | 0.8817 |
| 1 | whitespace | False | 2000 | 1 | 1.0 | 0.8807 |
| 1 | ws_only | False | 1000 | 2 | 0.001 | 0.8807 |
| 1 | bytelevel | False | 10000 | 2 | 0.01 | 0.8807 |
| 1 | whitespace | True | 1000 | 2 | 0.001 | 0.8797 |
| 1 | ws_only | False | 500 | 3 | 0.001 | 0.8797 |
| 1 | ws_only | False | 2000 | 1 | 1.0 | 0.8797 |
| 1 | bytelevel | False | 1000 | 2 | 0.01 | 0.8797 |
| 1 | whitespace | False | 10000 | 2 | 1.0 | 0.8787 |
| 1 | bytelevel | False | 500 | 3 | 0.001 | 0.8787 |
| 1 | bytelevel | False | 2000 | 2 | 0.01 | 0.8787 |
| 1 | whitespace | False | 1000 | 2 | 0.001 | 0.8777 |
| 1 | whitespace | True | 1000 | 3 | 0.1 | 0.8777 |
| 1 | bytelevel | False | 500 | 2 | 0.1 | 0.8777 |
| 1 | whitespace | False | 2000 | 2 | 0.001 | 0.8766 |
| 1 | whitespace | True | 500 | 3 | 0.01 | 0.8766 |
| 1 | whitespace | True | 10000 | 2 | 0.001 | 0.8766 |
| 1 | whitespace | False | 500 | 3 | 0.001 | 0.8746 |
| 1 | whitespace | True | 5000 | 2 | 0.001 | 0.8736 |
| 1 | bytelevel | False | 1000 | 2 | 0.001 | 0.8736 |
| 1 | bytelevel | False | 10000 | 2 | 1.0 | 0.8736 |
| 1 | whitespace | True | 10000 | 2 | 1.0 | 0.8726 |
| 1 | ws_only | False | 2000 | 3 | 1.0 | 0.8726 |
| 1 | ws_only | False | 5000 | 2 | 0.001 | 0.8726 |
| 1 | bytelevel | False | 2000 | 2 | 0.001 | 0.8726 |
| 1 | bytelevel | False | 2000 | 3 | 1.0 | 0.8726 |
| 1 | ws_only | False | 500 | 2 | 0.01 | 0.8716 |
| 1 | bytelevel | False | 1000 | 3 | 0.01 | 0.8716 |
| 1 | bytelevel | False | 2000 | 1 | 0.01 | 0.8716 |
| 1 | whitespace | True | 2000 | 3 | 1.0 | 0.8706 |
| 1 | ws_only | False | 10000 | 2 | 1.0 | 0.8706 |
| 1 | bytelevel | False | 2000 | 1 | 0.1 | 0.8706 |
| 1 | bytelevel | False | 2000 | 1 | 0.001 | 0.8706 |
| 1 | whitespace | False | 500 | 2 | 0.01 | 0.8696 |
| 1 | bytelevel | False | 2000 | 1 | 1.0 | 0.8696 |
| 1 | whitespace | False | 5000 | 2 | 0.001 | 0.8675 |
| 1 | ws_only | False | 2000 | 2 | 0.001 | 0.8675 |
| 1 | whitespace | True | 500 | 2 | 0.001 | 0.8665 |
| 1 | whitespace | True | 500 | 3 | 0.001 | 0.8665 |
| 1 | whitespace | True | 2000 | 3 | 0.1 | 0.8665 |
| 1 | ws_only | False | 2000 | 3 | 0.1 | 0.8665 |
| 1 | ws_only | False | 10000 | 2 | 0.01 | 0.8665 |
| 1 | bytelevel | False | 5000 | 2 | 0.001 | 0.8665 |
| 1 | bytelevel | False | 10000 | 2 | 0.001 | 0.8655 |
| 1 | whitespace | False | 2000 | 3 | 1.0 | 0.8635 |
| 1 | whitespace | False | 2000 | 3 | 0.1 | 0.8635 |
| 1 | whitespace | False | 10000 | 2 | 0.001 | 0.8635 |
| 1 | ws_only | False | 1000 | 3 | 0.01 | 0.8635 |
| 1 | bytelevel | False | 2000 | 3 | 0.1 | 0.8635 |
| 1 | bytelevel | False | 500 | 2 | 0.01 | 0.8615 |
| 1 | whitespace | False | 500 | 2 | 0.001 | 0.8595 |
| 1 | ws_only | False | 500 | 2 | 0.001 | 0.8595 |
| 1 | ws_only | False | 2000 | 3 | 0.01 | 0.8595 |
| 1 | whitespace | False | 1000 | 3 | 0.01 | 0.8584 |
| 1 | bytelevel | False | 2000 | 3 | 0.01 | 0.8574 |
| 1 | whitespace | True | 2000 | 3 | 0.01 | 0.8564 |
| 1 | bytelevel | False | 1000 | 3 | 0.001 | 0.8564 |
| 1 | bytelevel | False | 500 | 2 | 0.001 | 0.8544 |
| 1 | whitespace | False | 2000 | 3 | 0.01 | 0.8534 |
| 1 | whitespace | True | 1000 | 3 | 0.01 | 0.8534 |
| 1 | whitespace | True | 1000 | 1 | 0.01 | 0.8514 |
| 1 | whitespace | True | 1000 | 1 | 0.001 | 0.8514 |
| 1 | ws_only | False | 1000 | 1 | 1.0 | 0.8514 |
| 1 | ws_only | False | 1000 | 1 | 0.1 | 0.8514 |
| 1 | ws_only | False | 1000 | 1 | 0.01 | 0.8514 |
| 1 | ws_only | False | 1000 | 1 | 0.001 | 0.8514 |
| 1 | whitespace | True | 1000 | 1 | 0.1 | 0.8504 |
| 1 | whitespace | True | 1000 | 1 | 1.0 | 0.8483 |
| 1 | ws_only | False | 10000 | 2 | 0.001 | 0.8483 |
| 1 | bytelevel | False | 1000 | 1 | 0.1 | 0.8463 |
| 1 | bytelevel | False | 1000 | 1 | 0.01 | 0.8463 |
| 1 | bytelevel | False | 1000 | 1 | 0.001 | 0.8463 |
| 1 | bytelevel | False | 1000 | 1 | 1.0 | 0.8443 |
| 1 | bytelevel | False | 5000 | 3 | 0.1 | 0.8443 |
| 1 | whitespace | True | 5000 | 3 | 0.1 | 0.8433 |
| 1 | ws_only | False | 1000 | 3 | 0.001 | 0.8433 |
| 1 | whitespace | False | 1000 | 1 | 0.1 | 0.8423 |
| 1 | whitespace | False | 1000 | 1 | 0.01 | 0.8423 |
| 1 | whitespace | False | 1000 | 1 | 0.001 | 0.8423 |
| 1 | bytelevel | False | 5000 | 3 | 1.0 | 0.8423 |
| 1 | bytelevel | False | 5000 | 3 | 0.01 | 0.8423 |
| 1 | whitespace | False | 1000 | 1 | 1.0 | 0.8402 |
| 1 | whitespace | False | 1000 | 3 | 0.001 | 0.8402 |
| 1 | bytelevel | False | 2000 | 3 | 0.001 | 0.8392 |
| 1 | whitespace | True | 5000 | 3 | 0.01 | 0.8382 |
| 1 | whitespace | False | 5000 | 3 | 1.0 | 0.8372 |
| 1 | ws_only | False | 5000 | 3 | 1.0 | 0.8372 |
| 1 | bytelevel | False | 10000 | 3 | 0.1 | 0.8372 |
| 1 | whitespace | True | 1000 | 3 | 0.001 | 0.8362 |
| 1 | whitespace | False | 5000 | 3 | 0.1 | 0.8352 |
| 1 | ws_only | False | 5000 | 3 | 0.1 | 0.8352 |
| 1 | bytelevel | False | 10000 | 3 | 1.0 | 0.8352 |
| 1 | whitespace | False | 2000 | 3 | 0.001 | 0.8342 |
| 1 | whitespace | False | 10000 | 3 | 0.1 | 0.8342 |
| 1 | whitespace | True | 10000 | 3 | 0.1 | 0.8342 |
| 1 | whitespace | True | 5000 | 3 | 1.0 | 0.8332 |
| 1 | whitespace | False | 10000 | 3 | 1.0 | 0.8322 |
| 1 | whitespace | True | 2000 | 3 | 0.001 | 0.8311 |
| 1 | bytelevel | False | 10000 | 3 | 0.01 | 0.8311 |
| 1 | whitespace | True | 10000 | 3 | 1.0 | 0.8301 |
| 1 | whitespace | False | 10000 | 3 | 0.01 | 0.8291 |
| 1 | whitespace | False | 5000 | 3 | 0.01 | 0.8281 |
| 1 | whitespace | True | 10000 | 3 | 0.01 | 0.8281 |
| 1 | ws_only | False | 2000 | 3 | 0.001 | 0.8281 |
| 1 | ws_only | False | 5000 | 3 | 0.01 | 0.8281 |
| 1 | whitespace | True | 500 | 1 | 1.0 | 0.8231 |
| 1 | whitespace | True | 500 | 1 | 0.1 | 0.8231 |
| 1 | whitespace | True | 500 | 1 | 0.01 | 0.8231 |
| 1 | whitespace | True | 500 | 1 | 0.001 | 0.8231 |
| 1 | bytelevel | False | 5000 | 3 | 0.001 | 0.8220 |
| 1 | ws_only | False | 500 | 1 | 1.0 | 0.8200 |
| 1 | ws_only | False | 500 | 1 | 0.1 | 0.8200 |
| 1 | ws_only | False | 500 | 1 | 0.01 | 0.8200 |
| 1 | ws_only | False | 500 | 1 | 0.001 | 0.8200 |
| 1 | whitespace | True | 5000 | 3 | 0.001 | 0.8190 |
| 1 | whitespace | False | 500 | 1 | 1.0 | 0.8160 |
| 1 | whitespace | False | 500 | 1 | 0.1 | 0.8150 |
| 1 | whitespace | False | 500 | 1 | 0.01 | 0.8150 |
| 1 | whitespace | False | 500 | 1 | 0.001 | 0.8150 |
| 1 | bytelevel | False | 10000 | 3 | 0.001 | 0.8140 |
| 1 | whitespace | False | 10000 | 3 | 0.001 | 0.8129 |
| 1 | ws_only | False | 10000 | 3 | 0.01 | 0.8109 |
| 1 | whitespace | True | 10000 | 3 | 0.001 | 0.8099 |
| 1 | whitespace | False | 5000 | 3 | 0.001 | 0.8089 |
| 1 | ws_only | False | 10000 | 3 | 1.0 | 0.8049 |
| 1 | ws_only | False | 10000 | 3 | 0.1 | 0.8049 |
| 1 | ws_only | False | 5000 | 3 | 0.001 | 0.7937 |
| 1 | bytelevel | False | 500 | 1 | 1.0 | 0.7907 |
| 1 | bytelevel | False | 500 | 1 | 0.1 | 0.7907 |
| 1 | bytelevel | False | 500 | 1 | 0.01 | 0.7907 |
| 1 | bytelevel | False | 500 | 1 | 0.001 | 0.7907 |
| 1 | ws_only | False | 10000 | 3 | 0.001 | 0.7765 |
