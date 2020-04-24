PRG_Reader
==========

Decode microKorg .prg files and create a text representation of the patch in edit-select form.

e.g. will accept a .prg file downloaded from the microKorg into SoundEditor (and possibly modified) and create something like this:

```
New Name
[Voice]: Synth , Layer , Poly , -- , --  
[Pitch]: 0 , 0 cent , 0 , 2 , 5  
[Osc 1]: Saw , 0 , 0 , -- , --  
[Osc 2]: Saw , None , 0 , 0 , --  
[Mix Levels]: 127 , 0 , 0 , -- , --  
[Filter]: -12dB LP , 127 , 20 , 0 , 0  
[Filter EG]: 0 , 64 , 127 , 0 , yes  
[Amp]: 127 , cnt , off , 0 , --  
[Amp EG]: 0 , 64 , 127 , 0 , yes  
[LFO 1]: Triangle , Off , off , 10 , --  
[LFO 2]: Sine , Off , off , 70 , --  
[Patch 1]: LFO1 , Pitch , 0 , -- , --  
[Patch 2]: LFO2 , Pitch , 0 , -- , --  
[Patch 3]: LFO1 , Cutoff , 0 , -- , --  
[Patch 4]: LFO2 , Cutoff , 0 , -- , --
```