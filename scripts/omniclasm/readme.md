# State of Decay

Created by Omniclasm. (http://www.bay12forums.com/smf/index.php?topic=150782.0)  
Rewritten for PyDwarf by Sophie Kirschner. (http://www.pineapplemachine.com)

Collection of DFHack scripts that are somewhere between a "mod" and a "fps booster". Fully modular, you can pick and choose which scripts you want or don't want.

## starvingdead

This was the original script, and probably has the least impact on vanilla gameplay. It mostly helps prevent undead cascades in the caverns. What is an undead cascade? An undead cascade is when a forgotten beast kills a (living) troglodyte, then the now reanimated troglodyte kills the forgotten beast, then they both proceed to kill every living thing in the cavern. Then every previously living thing reanimates. Then they kill every other living thing. Then those reanimate as well, and next thing you know, you have 300+ undead roaming the caverns and destroying your FPS.

So, how does this script prevent that? With this script running, all undead that have been on the map for a time (default: 1 month) start to gradually decay, losing strength, speed, and toughness. After they have been on the map for even longer (default: 3 months), they collapse upon themselves, never to be reanimated.

Usage:
``` shell
starvingdead start
starvingdead stop
```

## deteriorate

These modules have a general concept of "use it or lose it". If something isn't being used, it quickly wears away until it no longer exists, freeing up some valuable FPS.

### corpses 

In long running forts, especially evil biomes, you end up with a lot of toes, teeth, fingers, and limbs scattered all over the place. Various corpses from various sieges, stray kitten corpses, probably some heads. Basically, your map will look like a giant pile of assorted body parts, all of which individually eat up a small part of your FPS, which collectively eat up quite a bit.

In addition, this script also targets various butchery byproducts. Enjoying your thriving animal industry? Your FPS does not. Those thousands of skulls, bones, hooves, and wool eat up precious FPS that could be used to kill goblins and elves. Whose corpses will also get destroyed by the script to kill more goblins and elves.

This script causes all of those to rot away into nothing after several months.

Usage:
``` shell
deterioratecorpses start
deterioratecorpses stop
```

### clothes 

This script is fairly straight forward. All of those slightly worn wool shoes that dwarves scatter all over the place will deteriorate at a greatly increased rate, and eventually just crumble into nothing. As warm and fuzzy as a dining room full of used socks makes your dwarves feel, your FPS does not like it.

Usage:
``` shell
deteriorateclothes start
deteriorateclothes stop
```

### food 

This script is...pretty far reaching. However, almost all long running forts I've had end up sitting on thousands and thousands of food items. Several thousand cooked meals, three thousand plump helmets, just as many fish and meat. It gets pretty absurd. And your FPS doesn't like it. With this script running, all food and plants wear out and disappear after several months. Barrels and stockpiles will keep them from rotting, but it won't keep them from decaying. No more sitting on a hundred years worth of food. No more keeping barrels of pig tails sitting around until you decide to use them. Either use it, eat it, or lose it. Seeds, are excluded from this, if you aren't planning on using your pig tails, hold onto the seeds for a rainy day.

Usage:
``` shell
deterioratefood start
deterioratefood stop
```
