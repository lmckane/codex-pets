# Clawd pet for Codex

Created from the original Clawd GIF assets in [Mascot Studio](https://github.com/Harriszed/mascot-studio). The source character, colors, pixel shapes, and activity frames are preserved. Frames were cropped and scaled into the ChatGPT Pets v2 grid. The source celebration supplies the jump frames with confetti removed. The original walking animation supplies rightward movement and its frames were mirrored for leftward movement. The sixteen required look poses move Clawd's original square eye pixels on the original body.

Source state mapping:

| Pet state | Mascot Studio GIF |
| --- | --- |
| idle | `idle-fluid.gif` |
| running-right | `walking-fluid.gif` |
| running-left | mirrored `walking-fluid.gif` frames |
| waving | `greeting-fluid.gif` |
| jumping | `done.gif` Clawd pixels |
| failed | `error.gif` |
| waiting | `waiting-for-you-fluid.gif` |
| running (active work) | `typing-fluid.gif` |
| review | `testing.gif` |

The final sheet is `run/final/spritesheet-extended.png`. The bundled Pets quality gate passed with subtle intermediate gaze warnings. The Pets service validated the exact PNG as v2 with 73 required frames and no structural errors.

Created pet ID: `pet_6b0649e9dc408191ae912758c46e1895`. It was not selected; Synki remains active.

The upstream repository's [NOTICE](https://github.com/Harriszed/mascot-studio/blob/main/NOTICE.md) says artwork redistribution permission remains unverified. Keep this pet personal unless that status changes.
