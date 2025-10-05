Project Mercury – Field‑Hockey‑Focused Research:

Introduction

The original Project Mercury design was built around ice‑hockey data, which differs substantially from outdoor field hockey. Field hockey is played on a turf field that is 91.40 m long and 55 m wide
fih.hockey
 and uses a spherical ball rather than a puck. Each team fields 11 players at a time
fih.hockey
, with the option of playing either with a fully equipped goalkeeper or solely with field players
fih.hockey
. To adapt the platform for field hockey analytics, this report summarizes official equipment specifications, pitch dimensions, team composition rules, bench and umpiring guidelines, and edge‑condition scenarios from recent (2023–2024) FIH and Field Hockey Canada documents. These details are then integrated into the Mercury architecture to ensure models, datasets and detectors align with field‑hockey realities.

Field‑Hockey Equipment and Specifications
Hockey Stick

Field‑hockey sticks have a traditional J‑ or U‑shaped head and a flat playing side. The International Hockey Federation (FIH) restricts sticks to specific dimensions and materials to ensure safety and consistency:

Length and weight: The stick must not exceed 105 cm in length (measured from the top of the handle to the bottom of the head) and must weigh no more than 737 g
fih.hockey
. These limits prevent excessive leverage and ensure that sticks can be swung safely.

Shape and curvature: Sticks are tested on a flat surface marked with reference lines (A, A1, B, B1, C and X). The maximum bow (rake) is 25 mm, and the point of maximum bow cannot be closer than 200 mm from the base of the head
fih.hockey
. The head must be flat on the left side and may only have a single convex or concave deviation of up to 4 mm
fih.hockey
; twists along the flat side are prohibited
fih.hockey
.

Materials: Sticks may be made of or contain any material except metal
fih.hockey
. Modern composite sticks typically blend carbon fibre, fibreglass and aramid for strength and lightweight performance
olympics.com
. The handle is usually wrapped with non‑slip tape for grip
olympics.com
.

Testing ring: To ensure the stick is not excessively thick, it must pass through a 51 mm‑diameter ring
fih.hockey
.

These measurements ensure that any computer‑vision model trained to detect sticks uses the correct scale (approx. 3 ft / 90–105 cm long) and shape. Models must also distinguish the flat playing side from the rounded back because players may not use the back of the stick during play.

Ball

The field‑hockey ball is spherical, usually made of hard plastic with possible dimples to aid travel on wet turf. According to the FIH rules:

Circumference: The ball must have a circumference of 224–235 mm
fih.hockey
 (approximately 22.4–23.5 cm). This translates to a diameter of 71.3–74.8 mm.

Weight: A regulation ball weighs 156–163 g
fih.hockey
.

Colour and surface: The ball is coloured white or a contrasting colour
fih.hockey
 and is hard with a smooth surface, though shallow indentations (dimples) are permitted
fih.hockey
. Indentations reduce friction on wet surfaces and should be considered when training detection models.

Pitch and Field Markings

The field‑hockey field of play is a synthetic turf surface with specific lines and areas:

Dimensions: The field is rectangular, 91.40 m long and 55.00 m wide
fih.hockey
.

Lines: Side‑lines mark the longer boundaries and back‑lines mark the shorter boundaries
fih.hockey
. A centre line divides the field into halves
fih.hockey
. Two 23 m lines are marked across the field 22.90 m from each back‑line
fih.hockey
.

Circles (shooting circles): Semi‑circular arcs, known as circles, are marked around each goal
fih.hockey
. Only shots taken inside the circle can score goals.

Penalty spots: A penalty spot 150 mm in diameter is located 6.40 m from the inner edge of each goal‑line
fih.hockey
.

Line width: All lines are 75 mm wide and are part of the field
fih.hockey
.

Flag posts: Posts 1.20–1.50 m high mark each corner of the field
fih.hockey
.

Goals: Goals sit outside the field and touch the back‑line
fih.hockey
. They comprise two posts 3.66 m apart and a crossbar 2.14 m high; a backboard (0.46 m high) and side boards of 1.20 m depth (dimensions taken from FIH goal specifications, not explicitly quoted in this document but part of standard FIH goals).

These dimensions are essential for spatial analytics (e.g., mapping trajectories onto a scaled 2D pitch). When calibrating cameras or creating a bird’s‑eye view, ensure the coordinate system matches the FIH pitch size.

Goalkeeper and Player Equipment

Goalkeeper protection: Hand protectors may be up to 228 mm wide and 355 mm long
fih.hockey
. Leg guards may be up to 300 mm wide
fih.hockey
. Computer‑vision models should therefore expect bulkier shapes for goalkeepers compared with field players.

Team clothing: Field players wear jerseys, shorts or skirts, shin guards and mouth guards. Goalkeepers wear helmets, chest guards, padded shorts, leg guards, kickers and gloves.

Team Benches and Technical Areas

Field‑hockey competition venues provide team benches near the technical table. Although the FIH rulebook does not specify bench dimensions, recent event manuals provide guidance:

Placement: Team benches must be on the same side of the pitch as the technical table
fieldhockey.ca
. Only the team manager and nominated substitute players may occupy the bench during play
fieldhockey.ca
.

Conduct: Team officials and substitutes must remain at or near the bench and may only coach from designated areas
fieldhockey.ca
. Non‑bench members must leave the field five minutes before the match starts
fieldhockey.ca
.

Equipment: In the FIH World Cup 2026 venue specifications, the benches should provide electrical outlets, running water, a stick‑storage box, waste bin, protective screens from the watering system, a 3 m² table for drinks and medical equipment, and cooling fans in hot climates
fih.hockey
. Team benches should preferably be near changing rooms
fih.hockey
. This ensures comfortable logistics for players and staff during matches.

These details matter for video analytics: cameras often capture benches and technical officials, so models should identify them as non‑playing entities. Benches also serve as substitution entry points, so automated tracking must handle players crossing the boundary near the 3‑metre substitution zone
fih.hockey
.

Composition of Teams and Umpiring
Players and Substitutions

Players on field: Each team fields up to 11 players at any time
fih.hockey
. Teams may choose to play with a fully equipped goalkeeper or with only field players
fih.hockey
.

Substitutions: There is no limit on the number of substitutions. Players leave or enter the field within 3 m of the centre line and time is not stopped except for goalkeeper substitutions
fih.hockey
. A player leaving the field due to injury, refreshment or equipment change must re‑enter between the two 23 m lines
fih.hockey
.

Match duration: Standard international matches consist of four periods of 15 minutes with 2‑minute breaks after the first and third periods and a 5‑minute half‑time (extendable to 10 minutes)
fieldhockey.ca
.

Umpires and Officials

Field umpires: Two umpires control the match. Each umpire is responsible for decisions in one half of the field and the circle to their right, but they often consult each other
en.wikipedia.org
. Umpires blow the whistle to start and end periods, award penalties, stop and restart time for penalty corners and strokes, and manage goalkeeper substitutions
fih.hockey
.

Technical bench: International matches include a technical bench comprising a technical officer, judges, timekeeper and record keeper. They ensure correct substitutions, manage the game clock and record warnings and suspensions.

Edge‑Condition Scenarios

Analytics systems must recognise conditions where play stops or rules alter:

Ball out of play: The ball is out of play when it completely crosses the side‑line or back‑line. A free hit is awarded at the location where the ball left the field, with opponents at least 5 m away
fih.hockey
.

Penalty corners: Awarded for intentional offences by defenders within their 23 m area or circle
fih.hockey
. During corners, the clock stops for 40 seconds to allow defenders to don protective gear
fieldhockey.ca
. Attackers inject the ball from the back‑line at least 10 m from the nearest goalpost; defenders must remain behind the back‑line until the ball is played.

Penalty strokes: Awarded for offences that prevent a probable goal
fih.hockey
. Taken from the penalty spot with only the striker and goalkeeper involved.

Free hits and 23 m rules: Free hits are taken close to where an offence occurred
fih.hockey
. Opponents must be 5 m away
fih.hockey
. Inside the attacking 23 m area, the ball must travel 5 m or be touched by a defender before entering the circle.

Scoring: A goal can only be scored from within the circle. Shots may be raised if they are not dangerous; deflections off defenders count if the initial shot was taken inside the circle.

Understanding these scenarios is crucial for designing event‑detection algorithms (e.g., penalty corner recognition, ball‑out events) and for aligning overlays with the game clock.

Implications for Project Mercury Architecture

The field‑hockey specifics above should inform modifications to the Project Mercury roadmap:

Dataset and Annotation: Few public datasets exist for field hockey. The team should create a field‑hockey dataset with bounding boxes and masks for players, sticks, ball, goal posts, umpires, benches and technical officials. Use FIH specifications to annotate object sizes appropriately and calibrate field boundaries to the 91.4 × 55 m pitch. Tools like Label Studio can help. Use SAM 2 for auto‑annotation and refine using manual corrections.

Object Detection & Tracking: Replace references to ice‑hockey pucks with field‑hockey balls and ensure the detector is trained on ball sizes (7.1–7.5 cm diameter). Sticks should be detected with their curved head orientation and length. YOLOv9 remains an appropriate detector due to its speed and accuracy, while BoT‑SORT or ByteTrack can track players and the ball across the larger field. The tracker must handle frequent player substitutions at the 3‑m zone and players temporarily leaving the field for injuries.

Pose & Biomechanics: RTMPose or BlazePose can still estimate player skeletons. However, because field hockey players frequently crouch and bend, models must be fine‑tuned on field‑hockey poses for accurate keypoint detection.

Event Detection: Adapt rule‑based logic to field‑hockey events (e.g., penalty corners, penalty strokes, long corners, goals). Machine‑learning models like VideoMAE can learn to recognise drag‑flicks, tackles and aerial passes. Accurate detection of the ball leaving the field or entering the circle will depend on precise pitch calibration.

Semantic Search & Output: The Librarian service should index clips based on field‑hockey events and incorporate metadata such as player positions, match time, and event type. The Herald service can overlay scoreboard information, penalty corner timers and substitution markers on the broadcast feed.

Conclusion

Adapting Project Mercury to outdoor field hockey requires careful attention to the sport’s equipment, field dimensions, player composition and edge‑condition rules. Official FIH documents specify that sticks must be under 105 cm and 737 g
fih.hockey
, balls between 224–235 mm circumference and 156–163 g
fih.hockey
, and pitches 91.40 m × 55 m with 23 m lines, circles and penalty spots
fih.hockey
. Team benches and technical areas must meet safety and logistical standards
fieldhockey.ca
fih.hockey
. By integrating these requirements into the dataset, detection models and event logic, the Mercury platform will provide accurate, reliable analytics for field‑hockey games and avoid confusion with ice‑hockey conventions.
