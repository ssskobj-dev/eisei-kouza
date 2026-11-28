# Mapping lanes for self-driving cars from space

Full transcript of the video.

Self-driving cars need a high-definition map of every lane and road edge. Building that map with survey vehicles is slow and costly, so today it covers only a tiny share of the world's roads. Can satellites help draw the first draft instead? In 2020, a Toyota group showed they can. In this video, we look at who used it, where it fits in the workflow, what the accuracy number really means, what satellites cannot see, and how to think about the cost.

## About Satellite to Decision

Satellite to Decision, which makes this video, publishes satellite data market reports and runs two certifications - Satellite Data Marketer, and Satellite Data Analysis Engineer. The website address and QR code are on screen.

## Where, who, and why

The case is a proof of concept by TRI-AD, a Toyota group company, together with Maxar Technologies and NTT DATA. In their 2019 announcement, they noted that high-definition maps then covered less than one percent of the world's road network. Survey vehicles are expensive, so coverage had been limited to highways. The idea was to use wide-area satellite imagery to draft maps of ordinary surface roads. The satellite work ran across Tokyo's twenty-three wards and six more cities around the world.

## Where it fits in the workflow

Here is where it fits. The satellite map is a first draft, made before the survey vehicles go out. First, you choose the cities and roads to map, and check whether the commercial archive has good enough imagery. Next, software extracts lanes and road edges from the image automatically. Then you flag the stretches the satellite could not see or could not map accurately, to fill another way. In-vehicle camera data corrects the draft and adds the content of signs and signals. Finally, survey vehicles are sent only to the stretches that are left. The satellite does not finish the map. It sets the order of work and decides where the survey vehicles go.

## Satellite versus people

The split of roles looks like this. The satellite images wide areas in one pass, extracts the lanes and road edges, and automatically removes the clutter that is not part of the map, such as parked cars, shadows, and the lean of tall buildings. People and in-vehicle cameras read the content of signs and signals, fill in what sits under elevated roads and inside tunnels, update the day-to-day changes, and verify the accuracy. The two sides are partners, not substitutes.

## What the 2020 proof of concept showed

Here is what the proof of concept reported, announced on March tenth, 2020. From the highest-resolution commercial satellite imagery, the team created maps with about twenty-five centimeters of relative accuracy, within Tokyo's twenty-three wards and six cities worldwide. A separate test using dash-cam data reached about forty centimeters. Overall, the release described relative accuracy of less than fifty centimeters for surface roads. One point matters here. The release attaches a footnote to the twenty-five and forty centimeter figures. They are reference values from parts of the test area where the data was especially good, not a guarantee for the whole area. And relative accuracy means the positions of features relative to each other, which is different from absolute position on the globe.

## Limits as of 2026

The limits are worth stating plainly. First, the twenty-five centimeter figure is a footnoted reference value for good conditions, not a result across the whole area. Second, parked cars, shadows, and the lean of tall buildings hide parts of the road, which is exactly why the method has to remove them. Third, anything under an elevated road, inside a tunnel, or beneath a roof is not visible from above. Fourth, the content of signs and signals cannot be read from directly overhead, so in-vehicle cameras cover that. Fifth, commercial high-resolution imaging is ordered on demand, not captured daily, so it is too infrequent for day-to-day changes such as roadworks. Note also that the release does not name the satellite used or its resolution, and no newer accuracy figures from this work have been published.

## Plans and training for organisations

A quick note. For organisations we offer in-house training and a corporate plan, so your whole team can use the market reports, use cases and training. See the form in the description.

## Why free satellites do not fit here

A fair question is whether free satellite data could do this. Here, it cannot. Free optical data, such as Europe's Sentinel-2, is about ten meters per pixel. A traffic lane is only about three meters wide, finer than a single free-data pixel, so lanes blur away. This is why the case relies on the highest-resolution commercial imagery, around thirty centimeters per pixel or better. Many satellite use cases run on free data. This is one that does not.

## How to think about the cost

Now the cost. The actual figures for this proof of concept were not disclosed, so this is how to think about it, not a quote. There are four parts. First is satellite imagery. Paid high-resolution imagery is required, free data does not work, and the price changes with area and how recent the image is. Second is analysis, the software that removes the clutter and extracts the map, built jointly by the three companies. Third is in-vehicle data, shown in the release as a separate test, so there is no combined price. And fourth, verification and survey vehicles, which do not go away. The announcement itself only says that update time, coverage, and build-and-maintain cost are expected to improve. It does not promise a specific saving.

## When it fits, and when it does not

Finally, where it fits. It fits when the goal is to draft wide areas first, on open surface roads, where what you need is the shape of lanes and road edges, on a yearly mapping cycle. It does not fit when you expect to finish the whole map from space alone, on roads hidden under structures or in dense narrow streets, where you need the content of signs and signals, or where you need daily updates. When you propose this, three points matter. Always quote the accuracy figure together with its footnote. Never say the satellite alone makes the map. And separate the cost into imagery, analysis, vehicle data, and verification, rather than promising one headline saving.

## Considering it for your fleet or map program?

To consider this for your own fleet or mapping program, here is the next step. We help you write the request for proposals and gather competitive quotes, independent of any satellite operator or analytics company. Use the form in the description to get in touch.

## Two certifications you can earn

One last thing. At Satellite to Decision you can earn two certifications - Satellite Data Analysis Engineer, and Satellite Data Marketer. If you want to turn what you learned into a credential, see the link in the description. Thanks for watching.
