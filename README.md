
Project Olympian: Field Hockey Analytics Platform


Solution Blueprint & Implementation Guide (Revision 2)

Project Codename: Mercury
Principal Investigator: Project Olympian
Date: October 5, 2025
Document Version: 2.0

Introduction: The Vision for Project Mercury

Project Mercury represents a paradigm shift in sports analytics. It is conceived not merely as a data-gathering tool, but as a comprehensive, end-to-end intelligence ecosystem for field hockey. The platform's core mission is to ingest raw video footage and transform it into multifaceted, actionable insights tailored for a diverse range of end-users.
This document serves as the definitive project book, expanding upon the revised architectural blueprint. It provides a deep, multidisciplinary exploration of the project's scope, the scientific and mathematical principles underpinning its analytical capabilities, the detailed software architecture, and a phased implementation roadmap. It is designed to be a living document, guiding developers, designers, and stakeholders from initial setup to full-scale commercial deployment.
The architecture is founded on an open-source-first, local-first philosophy. This ensures maximum flexibility, avoids vendor lock-in, and provides a clear, cost-effective pathway from a local development environment to a scalable, production-grade cloud infrastructure.

Stage 1: Problem Deconstruction & Scoping (Revised)


1.1. Core Objective (Refined)

To build an end-to-end platform that processes raw field hockey video, extracts detailed analytics, and delivers these insights through three distinct, high-quality channels:
A sophisticated analytics dashboard for coaches and analysts.
Dynamic graphical overlays on a processed video output for broadcasters and general audiences.
A flexible, well-documented API for third-party developers.

1.2. Target User Personas & Tailored Interfaces

The success of Project Mercury hinges on serving the unique needs of its distinct user groups. The architecture, particularly the Herald output layer, is explicitly designed to cater to the following personas:
Persona 1: The Coach/Analyst ("The Tactician")
Needs: Deep, granular data for pre-game strategy, post-game review, and individual player development. They require tools to dissect team formations, analyze set-piece effectiveness, and quantify player performance with objective metrics.
Platform Solution (Herald-Dashboard): An interactive, data-dense web application inspired by the rich interfaces of sports management simulations like Football Manager. This dashboard will prioritize data exploration and comparative analysis, featuring:
Multi-panel layouts to view tactical maps, player statistics, and event timelines simultaneously.1
Advanced visualizations like attribute polygons (spider charts) for quick player comparisons, passing network graphs, and territorial heatmaps.1
Interactive 2D replay of the entire game on a tactical map, allowing for scrubbing, annotation, and filtering by event.
Persona 2: The Broadcaster/General Audience ("The Fan")
Needs: Engaging, easily digestible visual information that enhances the viewing experience. They require context and narrative, transforming raw data into compelling on-screen graphics that explain the action in real-time.
Platform Solution (Herald-Renderer): An asynchronous video processing service that generates a new video file with broadcast-quality overlays, inspired by the "diegetic" UI of sports video games like FIFA 23. These are world-space graphics that appear integrated with the field of play:
Player-specific data: Nameplates, current speed, and distance covered, all tracked to the player's position on screen.
Event-based graphics: Perspective-correct shot trajectory trails, highlighted passing lanes, and player-specific spotlights during key moments.
Automated highlight reels with integrated graphics for key events like goals or penalty corners.
Persona 3: The Developer ("The Innovator")
Needs: A robust, reliable, and well-documented API to access the platform's rich dataset. They want to build custom applications, integrate Mercury's data into existing platforms, or conduct novel research.
Platform Solution (Herald-API): A flexible GraphQL API that allows developers to request exactly the data they need, no more and no less. This prevents the issues of over-fetching and under-fetching common with traditional REST APIs, making it highly efficient for a variety of unknown future applications.3

Stage 2: Factual Research & Literature Review (Expanded Focus)


2.1. Principles of Data Visualization and Storytelling

To serve our user personas effectively, the platform must not just present data, but tell stories with it. Effective data storytelling combines analytical interpretation with creative narrative elements to make complex information accessible and compelling.5
For the Coach/Analyst: The dashboard design will follow principles of information hierarchy and contextualization. The goal is to guide the user from high-level summaries down to granular details, a key pattern in effective sports dashboards.1
Multi-Panel Layouts: Inspired by Football Manager, the dashboard will allow users to see player stats, a 2D tactical view, and key performance indicators (KPIs) simultaneously, facilitating comparative analysis.1
Contextual Benchmarking: Individual data points are of limited value. All metrics will be presented with context, such as league, team, or positional averages, to provide a clear benchmark for performance.1
Attribute Polygons (Spider Charts): These charts are excellent for visually comparing multiple player attributes (e.g., speed, shot power, defensive actions) in a single, compact graphic.2
For the Broadcaster/Fan: The visual language must be immediate and intuitive. The key is transforming raw statistics into engaging narratives that enhance the live viewing experience.11
"Diegetic" UI Elements: Graphics will be integrated directly into the 3D space of the game (projected onto the 2D video). This requires a precise homography transformation to make overlays like player nameplates, shot trails, and highlighted passing lanes appear perspective-correct and attached to the field of play.
Real-Time Data Integration: The Herald-Renderer will leverage real-time analytics to generate graphics that emphasize player speed, endurance, or tactical shifts as they happen, making broadcasts more interactive and educational.11

Stage 3: Multidisciplinary Solution Blueprint (Revised)


3.1. Physics & Mathematical Model: The Homography Transformation

The ability to create world-space overlays for the broadcast output and accurate tactical maps for the coaching dashboard is entirely dependent on the homography transformation.
A homography is a mathematical mapping (represented by a 3x3 matrix) that relates the points on one plane to the corresponding points on another plane.13 In our context, it maps the 2D pixel coordinates of the field in a video frame (the source plane) to the 2D top-down coordinates of a real or virtual field hockey pitch (the destination plane).

Implementation:
Keypoint Detection: A computer vision model will be trained to detect key, static points on the field (e.g., corners of the goal, intersections of lines, penalty corner marks).
Point Correspondence: We will create a template map of a standard field hockey pitch with the known real-world coordinates of these keypoints.
Matrix Calculation: For each video frame, the detected keypoints (source points) and their known template coordinates (destination points) will be fed into OpenCV's cv2.findHomography function. This function requires at least four corresponding point pairs to calculate the homography matrix H.14 Using more points provides a more robust estimation.
Coordinate Transformation: Once H is known for a frame, we can use cv2.perspectiveTransform to map any pixel coordinate (e.g., a player's foot position) from the video frame to its corresponding top-down coordinate on the tactical map, and vice-versa.
Robustness Considerations:
Moving Camera: Since the camera moves, a new homography matrix must be calculated for every frame (or every few frames, with interpolation). This requires the keypoint detection model to be fast and reliable.
Occlusion & Limited View: The camera may zoom in, causing some keypoints to go off-screen. The system must be robust to this, using whichever keypoints are currently visible. This is why findHomography is preferred over getPerspectiveTransform, as the former can work with more than four points and find the best fit, making it more resilient to noisy or incomplete data.14
Lens Distortion: For maximum accuracy, camera lens distortion should be corrected before homography estimation. While complex, robust methods exist that can estimate distortion parameters concurrently with the homography.16 This will be a consideration for Phase 3 and beyond.

3.2. Computer Vision & ML Strategy (Refined)

Oracle (Cognitive Core) - Team Identification:
Challenge: Simple color clustering is unreliable for identifying teams due to variations in lighting, shadows, and complex jersey patterns.
Solution: A more robust, two-stage approach will be used. After the Tracker service detects a player and provides a bounding box, the cropped player image will be passed to a dedicated, lightweight image classification model.
Technology: A fine-tuned MobileNetV3 is an ideal choice. It is designed for high efficiency on resource-constrained hardware, making it perfect for this secondary classification task that needs to run for every player in every frame. It will be trained on a custom dataset of cropped player images to classify them into discrete categories: Team_A, Team_B, Goalkeeper_A, Goalkeeper_B, and Umpire.17
Tracker (Hawkeye - Object Tracking):
Model: The primary object detection model (e.g., YOLOv8 or YOLOv9) will be fine-tuned on a custom dataset.
Expanded Classes: The annotation schema will be expanded to include four primary classes: player, ball, stick, and umpire. This allows the system to track officials separately and provides the necessary data for stick-based biomechanical analysis in later phases.
Chronicler (Clio - Event Detection):
Expanded Rules-Based Engine: The event detection module will be enhanced to identify key set-piece situations. This will be achieved by creating a rules-based engine that analyzes the spatial configuration of players and the ball relative to the field markings (whose real-world positions are known via the homography).
Example Rule for penalty_corner:
Condition: Ball is stationary within 1 meter of the baseline, inside the shooting circle.
Condition: At least four defending players are positioned behind the baseline, near the goal.
Condition: Multiple attacking players are positioned around the edge of the shooting circle.
Trigger: If all conditions are met for a continuous duration (e.g., > 2 seconds), classify the event as penalty_corner_setup.

Stage 4: Software & System Architecture (Major Revision)

The revised architecture expands the Herald service into a specialized suite of three components, each tailored to a specific user persona. This decoupled design is crucial for scalability and maintainability.

4.1. High-Level Architecture (Refined)

The data flows from the Nexus database layer to the new Herald suite:
Nexus (Databases) → Herald-API (GraphQL) →
Herald-Dashboard (Web App for Coaches)
Herald-Renderer (Video Processor for Broadcast)
Third-Party Applications (via API)

4.2. Technology Stack & Component Deep Dive

This section details the specific technologies chosen for the output layer and the rationale behind each decision.

API Layer: Herald-API

Technology: GraphQL served via a Python backend using FastAPI and Strawberry.
Design Rationale (Why GraphQL?):
Efficiency for Multiple Clients: GraphQL is the ideal choice for this architecture because our two primary front-ends have vastly different data requirements. The Herald-Dashboard needs large, complex datasets (e.g., all trajectory data for a full game), while the Herald-Renderer might only need event timestamps and player IDs for a specific highlight clip. With a traditional REST API, we would either create many specific endpoints or a few general ones that result in over-fetching. GraphQL solves this by allowing each client to specify exactly the data fields it needs in a single request, improving performance and reducing network load.3
Strongly-Typed & Self-Documenting: The GraphQL schema serves as a contract between the front-end and back-end, reducing integration errors. It is also introspective, meaning developer tools can automatically generate documentation, which is essential for serving our third-party developer persona.3
Implementation (Strawberry & FastAPI):
Strawberry is a modern Python GraphQL library that uses Python type hints to define the schema, making it feel native to Python and very similar to how FastAPI uses Pydantic models. This creates a consistent and intuitive developer experience.19
FastAPI provides the high-performance ASGI web server framework. Strawberry integrates seamlessly via its GraphQLRouter, allowing the GraphQL endpoint to coexist with other potential REST endpoints (e.g., for health checks) in the same application.20

Dashboard: Herald-Dashboard

Technology: React/Next.js frontend with Recharts for standard charts and Deck.gl for tactical visualizations.
Design Rationale & Implementation:
Framework (React/Next.js): Chosen for its robust ecosystem, performance optimizations (server-side rendering with Next.js), and vast developer community.
Standard Charts (Recharts): For displaying KPIs, timelines, and player stats, Recharts is the recommended library. It is a "drop-in, batteries included" library that is easy to learn and integrates seamlessly with React's component-based philosophy.25 While
Nivo offers a wider variety of chart types, its documentation can be less clear, and it can have responsiveness issues, making Recharts a more reliable and faster choice for the core dashboard functionality.25
Tactical Map (Deck.gl): Standard charting libraries are not designed to render tens of thousands of data points (e.g., every player's position for every frame) in an interactive way. Deck.gl is a GPU-powered, high-performance visualization framework specifically for large-scale datasets.29 It will be used to create the 2D tactical view, rendering player positions, trajectories, and heatmaps as layers on a canvas. Its layered approach allows for complex, interactive visualizations where users can toggle different data views on and off.29

Video Overlay Engine: Herald-Renderer

Technology: A Python worker service using Celery for task queuing and MoviePy/OpenCV for video manipulation.
Design Rationale & Implementation:
Asynchronous Processing (Celery): Video rendering is a computationally expensive and time-consuming process. Performing this task synchronously within an API request would lead to timeouts and a poor user experience. Celery is an industry-standard distributed task queue that solves this problem. When a user requests a rendered video, the Herald-API will create a rendering "task" and place it on a message queue (e.g., Redis or RabbitMQ). A separate pool of Celery worker processes will pick up these tasks and execute them in the background, independent of the API service.31
Video Manipulation (MoviePy & OpenCV):
MoviePy is a high-level library for video editing. It will be used for tasks like loading the source video, creating text and image overlays (e.g., player nameplates), compositing these overlays onto the main video clip, and encoding the final output file.38
OpenCV will be used for more granular, frame-by-frame drawing operations that require the homography transformation, such as drawing perspective-correct shot trails or highlighting areas of the pitch. The renderer will iterate through frames, use OpenCV to draw these complex graphics, and then composite them using MoviePy.

4.3. Local Deployment Strategy

The entire multi-service stack will be defined in a docker-compose.yml file. This is a cornerstone of the "local-first" development strategy. A single docker-compose up command will launch all the necessary containers: the backend Python services, the Nexus databases (Postgres, Weaviate), the Celery message broker (Redis), and the frontend React development server. This ensures a consistent, reproducible development environment for all team members and simplifies the transition to a production environment.

Stage 5: Implementation & Deployment Roadmap (Revised)

This roadmap is structured to deliver tangible value to the different user personas at each phase.

Phase 0: Foundation & Data Strategy (Weeks 1-4)

Objective: Establish the project's technical foundation and a rich data annotation pipeline.
Key Activities:
Infrastructure: Define the complete docker-compose.yml file for all services.
Annotation Schema: In CVAT, define a comprehensive annotation project including classes for player_teamA, player_teamB, umpire, ball, and stick.
Data Ingestion: Build the Harvester service to process initial videos.
Success Metrics: A developer can clone the repository and launch the entire local development environment with a single command. An initial batch of 10 videos is fully annotated.

Phase 1: MVP - The Core Data Pipeline & Dual Output (Weeks 5-14)

Objective: Prove the end-to-end concept by creating both a basic video overlay and a simple data dashboard from a single uploaded video.
Key Activities:
Backend: Build the core services (Harvester through Nexus). Fine-tune YOLOv8 for player, umpire, and ball.
API: Develop the Herald-API with basic GraphQL queries for retrieving trajectory and event data.
Dashboard: Build a single-page Herald-Dashboard using Deck.gl to display the 2D animated tactical map.
Renderer: Build a basic Herald-Renderer script that can produce a video with simple circular markers tracking each player and the ball, using data from the API.
Success Metrics: A user can upload a video via an API call and receive two outputs: a new MP4 video file with tracking overlays, and a web link to a 2D replay of the match.

Phase 2: Coach-Centric Features & Advanced Analytics (Weeks 15-22)

Objective: Build out the Herald-Dashboard into a powerful tool for coaches.
Key Activities:
CV: Implement the MobileNetV3 team/jersey identification model in the Oracle service.
Dashboard: Add advanced visualizations: heatmaps, passing networks, and player-specific stats pages with Recharts-powered attribute polygons (spider charts).
Event Detection: Implement the rules-based engine for set-piece events (penalty_corner, long_corner).
Renderer: Enhance Herald-Renderer with basic broadcast-style graphics like player name/speed tags.
Success Metrics: The dashboard provides at least 5 meaningful tactical and physical metrics (e.g., possession %, territory dominance, sprint counts). The rendered video can automatically highlight goals and shots with simple text overlays.

Phase 3: Broadcast Features & Biomechanics (Weeks 23-30)

Objective: Enhance the Herald-Renderer with FIFA-style graphics and add initial biomechanical analysis.
Key Activities:
CV: Develop the Atlas service using yolov8-pose for 2D keypoint extraction.
Dashboard: Add a "Biomechanics" tab to the player view, showing stick-figure replays of key actions (e.g., hits, drag-flicks).
Renderer: Enhance Herald-Renderer to draw advanced, homography-corrected overlays like shot trajectory trails and highlighted players.
Success Metrics: The renderer can produce a 1-minute highlight reel with engaging graphics for a full match. Biomechanical data (e.g., key joint angles) is available for at least two distinct player actions.

Phase 4 & 5: Production, API, & Commercialization (Weeks 31+)

Objective: Harden the platform, fully document the Herald-API for third-party use, and migrate to a scalable cloud environment.
Key Activities:
API Documentation: Create a comprehensive developer portal for the Herald-API.
Cloud Migration: Transition the Docker Compose setup to a cloud-native environment using Kubernetes for service orchestration and managed database services (e.g., AWS RDS for TimescaleDB, managed Weaviate cluster).
Onboarding: Onboard initial beta partners to use the API and dashboard, gathering feedback for further refinement.
Success Metrics: API has >99.9% uptime. Onboard 5 beta partners. Achieve first dollar of API revenue.
Works cited
