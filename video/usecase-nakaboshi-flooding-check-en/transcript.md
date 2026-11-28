# Checking rice-paddy carbon credits with satellite SAR

Full transcript of the video.

Can a satellite prove that a rice farmer extended mid-season drainage for a carbon credit? Not on its own. The answer is to use satellites as a screening check, flagging the paddies whose satellite record does not match the farmer's report, while records and photos stay the official evidence. In Japan, this is being tested by the space agency and private companies. In this video, we look at who uses it, where it fits in the workflow, what it can decide, how far free satellites go, and what paid imagery would cost.

## About Satellite to Decision

Satellite to Decision, which makes this video, publishes satellite data market reports and runs two certifications - Satellite Data Marketer, and Satellite Data Analysis Engineer. The website address and QR code are on screen.

## Where, who, and why

Here is the setting. Mid-season drainage means draining a rice paddy for one to two weeks mid-growth to dry the field. Japan's carbon-credit methodology rewards extending that drainage by at least seven days beyond the farmer's own two-year average, because it cuts methane, and rice paddies are Japan's largest source of methane. The methodology credits the extension with a thirty percent cut. The buyers here are the aggregators and verifiers who bundle many farmers and get audited together. As the number of member farmers grows, confirming every record and photo becomes a heavy load. So satellites are tested to screen the declarations.

## Where it fits in the workflow

Here is where it fits. It goes in before the audit, as an internal check. First, you collect the plot boundary data, because without it you cannot tell which satellite pixel belongs to which paddy. Then, across the drainage window, you line up each SAR observation and build a time series of when water was present and when it drained. You compare that against the farmer's declared start and end dates, and pull out the paddies that do not match. Only those paddies are asked for extra photos or records. The audit itself still runs on records and photos, exactly as the scheme requires. The satellite does not replace the evidence. It decides where to look harder.

## Satellite versus people

The split of roles looks like this. The satellite builds a flooding and draining time series for each paddy and flags the ones that do not match the farmer's report. The people gather the records and photos the scheme requires, ask the flagged paddies for extra proof, and decide, farmer by farmer, whether to keep draining or to re-flood to protect the yield. That last call is a human one, looking at the state of the crop. Note the scale here. This is still a demonstration stage. The space agency and several companies have run field trials, one covering about one hundred hectares. The accuracy and the match rate have not been published.

## What it can decide

Here is the data you receive and what it lets you decide. The flooding time series tells you which declarations match and which to question. The list of paddies that do not match tells you which ones to ask for extra proof. An estimate of past draining dates helps you check a farmer's baseline where records are thin. And the list of observation gaps tells you how many days the satellite cannot speak to at all. That last one is the real boundary of this method. Sizing that gap first, on a small area, lets you judge how much the check is worth.

## Limits as of 2026

The limits are stated plainly in the sources too. First, the official evidence is records and photos. The satellite judgment does not stand in for them at audit. Second, free SAR revisits every twelve to fourteen days, which is coarser than the seven-day rule, so a day of re-flooding between two passes is invisible. Third, the hope that longer-wave radar can see water under a full rice canopy is still being verified, not proven. Fourth, the accuracy has not been published. Comparison with ground water-level sensors only began in twenty twenty-five. And fifth, whether to extend the drainage or re-flood to save the yield is a human decision, looking at the crop, not something the satellite makes.

## Satellite data certifications

A quick note. If you want to turn what you learn into a credential, there are two certifications - Satellite Data Marketer, and Satellite Data Analysis Engineer. More at the end of the video and in the description.

## How far do free satellites go?

So how far can free satellites take you? Europe's Sentinel-1 is free, a C-band radar that revisits about every twelve days with one satellite. Whether a paddy is flooded or drained can be read from how the radar brightness changes through the season, at zero data cost. A flooded paddy is smooth, so the radar bounces away and the paddy looks dark; a dry or harvested field is rough and looks bright. On the other hand, a twelve-day gap cannot pin down a seven-day drainage window, and shorter C-band radar sees under a thick rice canopy less well than the longer-wave radar the demonstrations use. So free data is enough to try the screening, not to settle a borderline case.

## What paid imagery would cost (estimate)

Here is an estimate, a calculation with assumptions, not a quote. For free, Sentinel-1 radar costs nothing and is enough to screen, though it is weaker under the canopy. For paid imagery, the space agency's longer-wave radar satellite sees under the canopy better; its public price is about eighty thousand yen before tax for a fifty kilometre scene, from the Ministry of the Environment manual revised in March twenty twenty-six, and one scene covers a very large area. Assume a few passes across the drainage window. The bigger costs are not the imagery. They are preparing the plot boundary data, verifying the judgment against the ground, and running the analysis each season. Weigh all of that against the credit revenue. A model example in the methodology earns about one thousand eight hundred fifty yen per ten ares, at five thousand yen a tonne. That is a model figure, not an actual result, and prices change, so always confirm with a real quote.

## When it fits, and when it does not

Finally, where it fits. It fits where hundreds of paddies make record-checking heavy, where plots are large enough for the pixel to sit inside, where you need to flag declarations that do not match, and where the plot boundaries are already digitised. And it fits as an internal screening check, not as evidence. It does not fit where there are only a few dozen paddies you could review by hand, where plots are small and fragmented, where you need day-level proof of the start and end dates, where you do not know the boundaries, or where you hoped the satellite could be the audit evidence itself. When you propose this, three points matter. Ask about the plot boundary data and the paddy count first. Never say the satellite proves the credit. And put a number on the observation gaps before you promise anything.

## Considering it for your scheme?

To consider this for your own scheme or client, here is the next step. We help you write the RFP and gather competitive quotes, independent of any satellite operator or analytics company. Use the form in the description to get in touch.

## Two certifications you can earn

One last thing. At Satellite to Decision you can earn two certifications - Satellite Data Analysis Engineer, and Satellite Data Marketer. If you want to turn what you learned into a credential, see the link in the description. Thanks for watching.
