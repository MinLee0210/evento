# Inference time record

We collect all queries of all rounds, exlude the final round. There are 90 queries in total. We measure the the response time of the system. We only care 200 status code response. 


| Top K | Embedding | Smart Query | Mean | SD | Median | 
| --- | --- | --- | --- | --- | --- | 
| 20  | `clip` | `plain` | 1.0972 | 0.5347 | 0.7120 | 
| 20  | `clip` | `exploit` | 1.0040 | 0.8092 | 0.6734 | 
| 20  | `clip` | `explore` | 0.8390 | 0.3840 | 0.6737 | 
| 20  | `blip` | `plain` | 0.7379 | 0.2527 | 0.6679 | 
| 20  | `blip` | `exploit` | 0.7594 | 0.3076 | 0.6723 | 
| 20  | `blip` | `explore` | 0.7428 | 0.2976  | 0.6632 | 
| 20  | `blip_fct` | `plain` | 0.7382 | 0.2283 | 0.6668 | 
| 20  | `blip_fct` | `exploit` | 0.7712 | 0.4343 | 0.6771 | 
| 20  | `blip_fct` | `explore` | 0.6887 | 0.0622 | 0.6727 | 
| 20  | `blip_des` | `plain` | 0.6939 | 0.0699 | 0.6690 | 
| 20  | `blip_des` | `exploit` | 0.6716  | 0.0315 | 0.6625 | 
| 20  | `blip_des` | `explore` | 0.6814  | 0.0795 | 0.6641 | 