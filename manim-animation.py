"""
Manim animation script for visualizing the MCP Waifu Chat Server architecture and data flow.

This script creates a comprehensive animated explanation of the system, including:
- System architecture with layered components
- Data flow through the 7-step message processing pipeline
- AI provider system with OpenRouter and Gemini integration
- Database system with SQLite schema visualization
- Configuration system with priority-based loading

The animation is designed for educational and presentation purposes, showing how
different components interact within the MCP Waifu Chat Server ecosystem.
"""

from manim import *
import numpy as np

class MCPWaifuChatExplanation(Scene):
    def construct(self):
        # Title
        title = Text("MCP Waifu Chat Server", font_size=48, color=BLUE)
        subtitle = Text("Architecture & Flow Explanation", font_size=32, color=BLUE_B)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Architecture Overview
        self.show_architecture()

        # Data Flow
        self.show_data_flow()

        # AI Provider System
        self.show_ai_providers()

        # Database System
        self.show_database_system()

        # Configuration System
        self.show_config_system()

        # Conclusion
        self.show_conclusion()

    def show_architecture(self):
        section_title = Text("1. System Architecture", font_size=36, color=YELLOW)
        self.play(Write(section_title))
        self.wait(1)
        self.play(section_title.animate.to_edge(UP))

        # --- Construct all components FIRST, without animating ---

        # Client
        client = Rectangle(width=3, height=1, color=BLUE).set_fill(BLUE, opacity=0.2)
        client_label = Text("MCP Client", font_size=20)
        client_group = VGroup(client, client_label)

        # Server components
        server_box = Rectangle(width=6, height=4, color=GREEN).set_fill(GREEN, opacity=0.1)

        # API Layer - Create shape and label, then group them
        api_layer_shape = Rectangle(width=5, height=0.8, color=BLUE_B).set_fill(BLUE_B, opacity=0.3)
        api_label = Text("FastMCP API Layer", font_size=16)
        api_layer = VGroup(api_layer_shape, api_label)

        # AI Layer - Create shape and label, then group them
        ai_layer_shape = Rectangle(width=5, height=0.8, color=PURPLE).set_fill(PURPLE, opacity=0.3)
        ai_label = Text("AI Provider Layer", font_size=16)
        ai_layer = VGroup(ai_layer_shape, ai_label)

        # DB Layer - Create shape and label, then group them
        db_layer_shape = Rectangle(width=5, height=0.8, color=ORANGE).set_fill(ORANGE, opacity=0.3)
        db_label = Text("SQLite Database", font_size=16)
        db_layer = VGroup(db_layer_shape, db_label)

        # Config Layer - Create shape and label, then group them
        config_layer_shape = Rectangle(width=5, height=0.8, color=RED).set_fill(RED, opacity=0.3)
        config_label = Text("Configuration", font_size=16)
        config_layer = VGroup(config_layer_shape, config_label)

        # Arrange layers
        layers = VGroup(api_layer, ai_layer, db_layer, config_layer).arrange(DOWN, buff=0.1)
        layers.move_to(server_box.get_center())
        server_group = VGroup(server_box, layers)

        # Arrange client and server
        components = VGroup(client_group, server_group).arrange(RIGHT, buff=1.5)

        # External services
        openrouter = Rectangle(width=2, height=0.6, color=MAROON).set_fill(MAROON, opacity=0.3)
        openrouter_label = Text("OpenRouter", font_size=14)
        openrouter_group = VGroup(openrouter, openrouter_label).next_to(ai_layer, RIGHT, buff=1)

        gemini = Rectangle(width=2, height=0.6, color=TEAL).set_fill(TEAL, opacity=0.3)
        gemini_label = Text("Gemini", font_size=14)
        gemini_group = VGroup(gemini, gemini_label).next_to(openrouter_group, DOWN, buff=0.5)

        # Add arrows
        arrow1 = Arrow(client_group.get_right(), api_layer.get_left(), color=WHITE)
        arrow2 = Arrow(api_layer.get_bottom(), ai_layer.get_top(), color=WHITE)
        arrow3 = Arrow(ai_layer.get_bottom(), db_layer.get_top(), color=WHITE)
        arrow4 = Arrow(db_layer.get_bottom(), config_layer.get_top(), color=WHITE)
        arrow5 = Arrow(ai_layer.get_right(), openrouter_group.get_left(), color=WHITE)
        arrow6 = Arrow(ai_layer.get_right(), gemini_group.get_left(), color=WHITE)

        # --- Create the MASTER GROUP ---
        full_diagram = VGroup(
            components, openrouter_group, gemini_group,
            arrow1, arrow2, arrow3, arrow4, arrow5, arrow6
        )

        # --- Scale and Position the Master Group ---
        full_diagram.scale(0.85).next_to(section_title, DOWN, buff=0.3)

        # --- Now, animate the appearance ---
        self.play(FadeIn(full_diagram))
        self.wait(3)
        self.play(FadeOut(section_title), FadeOut(full_diagram))

    def show_data_flow(self):
        section_title = Text("2. Data Flow", font_size=36, color=YELLOW)
        self.play(Write(section_title))
        self.wait(1)
        self.play(section_title.animate.to_edge(UP))

        # --- Construct all components FIRST, without animating ---

        # Step 1: User sends message
        step1 = Rectangle(width=4, height=0.8, color=BLUE).set_fill(BLUE, opacity=0.2)
        step1_text = Text("1. User sends chat message", font_size=18)
        step1_group = VGroup(step1, step1_text)

        # Step 2: API receives request
        step2 = Rectangle(width=4, height=0.8, color=GREEN).set_fill(GREEN, opacity=0.2)
        step2_text = Text("2. FastMCP tool processes", font_size=18)
        step2_group = VGroup(step2, step2_text)

        # Step 3: Get dialog history
        step3 = Rectangle(width=4, height=0.8, color=ORANGE).set_fill(ORANGE, opacity=0.2)
        step3_text = Text("3. Retrieve dialog from DB", font_size=18)
        step3_group = VGroup(step3, step3_text)

        # Step 4: Construct prompt
        step4 = Rectangle(width=4, height=0.8, color=PURPLE).set_fill(PURPLE, opacity=0.2)
        step4_text = Text("4. Build AI prompt", font_size=18)
        step4_group = VGroup(step4, step4_text)

        # Step 5: Generate response
        step5 = Rectangle(width=4, height=0.8, color=PURPLE).set_fill(PURPLE, opacity=0.2)
        step5_text = Text("5. AI generates response", font_size=18)
        step5_group = VGroup(step5, step5_text)

        # Step 6: Save dialog
        step6 = Rectangle(width=4, height=0.8, color=RED).set_fill(RED, opacity=0.2)
        step6_text = Text("6. Update dialog in DB", font_size=18)
        step6_group = VGroup(step6, step6_text)

        # Step 7: Return response
        step7 = Rectangle(width=4, height=0.8, color=TEAL).set_fill(TEAL, opacity=0.2)
        step7_text = Text("7. Return AI response", font_size=18)
        step7_group = VGroup(step7, step7_text)

        # Arrange steps vertically
        all_steps = VGroup(step1_group, step2_group, step3_group, step4_group,
                          step5_group, step6_group, step7_group).arrange(DOWN, buff=0.3)

        # Add arrows between steps
        arrows = VGroup()
        for i in range(len(all_steps) - 1):
            arrow = Arrow(all_steps[i].get_bottom(), all_steps[i+1].get_top(),
                         color=WHITE, stroke_width=3)
            arrows.add(arrow)

        # --- Create the MASTER GROUP ---
        full_diagram = VGroup(all_steps, arrows)

        # --- Scale and Position the Master Group ---
        full_diagram.scale(0.8).next_to(section_title, DOWN, buff=0.2)

        # --- Now, animate the appearance ---
        self.play(Create(all_steps))
        self.play(Create(arrows))

        # Highlight the flow (this will work on the scaled version)
        self.wait(2)
        for i in range(len(all_steps)):
            self.play(all_steps[i].animate.scale(1.1), run_time=0.3)
            self.play(all_steps[i].animate.scale(1/1.1), run_time=0.3)

        self.wait(2)
        self.play(FadeOut(section_title), FadeOut(full_diagram))

    def show_ai_providers(self):
        section_title = Text("3. AI Provider System", font_size=36, color=YELLOW)
        self.play(Write(section_title))
        self.wait(1)
        self.play(section_title.animate.to_edge(UP))

        # --- Construct all components FIRST, without animating ---

        # Provider selection logic
        provider_logic = Rectangle(width=6, height=1.5, color=PURPLE).set_fill(PURPLE, opacity=0.2)
        provider_text = Text("Provider Selection Logic", font_size=20)
        provider_group = VGroup(provider_logic, provider_text)

        # OpenRouter branch
        openrouter_box = Rectangle(width=3, height=1, color=PURPLE).set_fill(PURPLE, opacity=0.2)
        openrouter_label = Text("OpenRouter (Default)", font_size=16)
        openrouter_group = VGroup(openrouter_box, openrouter_label).next_to(provider_group, DOWN, buff=1)

        # Gemini branch
        gemini_box = Rectangle(width=3, height=1, color=TEAL).set_fill(TEAL, opacity=0.2)
        gemini_label = Text("Gemini (Fallback)", font_size=16)
        gemini_group = VGroup(gemini_box, gemini_label).next_to(openrouter_group, RIGHT, buff=1)

        # Configuration sources
        config_sources = VGroup()

        env_var = Circle(radius=0.4, color=GREEN).set_fill(GREEN, opacity=0.3)
        env_text = Text("Environment\nVariables", font_size=12, line_spacing=0.8)
        env_group = VGroup(env_var, env_text).next_to(openrouter_group, DOWN, buff=1)

        dotfile = Circle(radius=0.4, color=BLUE).set_fill(BLUE, opacity=0.3)
        dotfile_text = Text("Dotfiles\n(~/.api-*)\n(~/.model-*)", font_size=12, line_spacing=0.8)
        dotfile_group = VGroup(dotfile, dotfile_text).next_to(env_group, RIGHT, buff=1)

        # Arrows
        arrow1 = Arrow(provider_group.get_bottom(), openrouter_group.get_top(), color=WHITE)
        arrow2 = Arrow(provider_group.get_bottom(), gemini_group.get_top(), color=WHITE)
        arrow3 = Arrow(openrouter_group.get_bottom(), env_group.get_top(), color=WHITE)
        arrow4 = Arrow(openrouter_group.get_bottom(), dotfile_group.get_top(), color=WHITE)
        arrow5 = Arrow(gemini_group.get_bottom(), env_group.get_top(), color=WHITE)
        arrow6 = Arrow(gemini_group.get_bottom(), dotfile_group.get_top(), color=WHITE)

        # Priority labels
        priority1 = Text("1st", font_size=14, color=YELLOW).next_to(env_group, LEFT)
        priority2 = Text("2nd", font_size=14, color=YELLOW).next_to(dotfile_group, LEFT)
        priority3 = Text("3rd", font_size=14, color=YELLOW).next_to(openrouter_group, DOWN, buff=2.5)

        # --- Create the MASTER GROUP ---
        full_diagram = VGroup(
            provider_group, openrouter_group, gemini_group,
            env_group, dotfile_group,
            arrow1, arrow2, arrow3, arrow4, arrow5, arrow6,
            priority1, priority2, priority3
        )

        # --- Scale and Position the Master Group ---
        full_diagram.scale(0.8).next_to(section_title, DOWN, buff=0.3)

        # --- Animate ---
        self.play(FadeIn(full_diagram))
        self.wait(3)
        self.play(FadeOut(section_title), FadeOut(full_diagram))

    def show_database_system(self):
        section_title = Text("4. Database System", font_size=36, color=YELLOW)
        self.play(Write(section_title))
        self.wait(1)
        self.play(section_title.animate.to_edge(UP))

        # --- Construct all components FIRST, without animating ---

        # Database schema
        schema = Rectangle(width=6, height=3, color=ORANGE).set_fill(ORANGE, opacity=0.2)
        schema_title = Text("SQLite Database Schema", font_size=20).next_to(schema, UP)

        # Table structure
        table_code = Text(
            """CREATE TABLE dialogs (
    current_user TEXT NOT NULL,
    user_id TEXT NOT NULL,
    dialog TEXT,
    last_modified_datetime TEXT,
    last_modified_timestamp INTEGER,
    PRIMARY KEY (current_user, user_id)
)""",
            font_size=16,
            font="monospace"
        )

        schema_group = VGroup(schema, schema_title, table_code)

        # Database operations
        operations = VGroup()

        ops = ["add_user_to_db", "get_old_dialog", "update_user_dialog",
               "reset_user_chat", "is_user_id_in_db", "delete_user_from_db"]

        for i, op in enumerate(ops):
            op_box = Rectangle(width=2.5, height=0.6, color=BLUE_B).set_fill(BLUE_B, opacity=0.3)
            op_text = Text(op, font_size=14)
            op_group = VGroup(op_box, op_text)
            operations.add(op_group)

        operations.arrange_in_grid(rows=3, cols=2, buff=0.3).next_to(schema_group, RIGHT, buff=1)

        # Connection pooling
        conn_pool = Rectangle(width=3, height=0.8, color=GREEN).set_fill(GREEN, opacity=0.3)
        conn_text = Text("Connection Pooling", font_size=16)
        conn_group = VGroup(conn_pool, conn_text).next_to(schema_group, DOWN, buff=1)

        # --- Create the MASTER GROUP ---
        full_diagram = VGroup(schema_group, operations, conn_group)

        # --- Scale and Position the Master Group ---
        full_diagram.scale(0.8).next_to(section_title, DOWN, buff=0.3)

        # --- Animate ---
        self.play(FadeIn(full_diagram))
        self.wait(3)
        self.play(FadeOut(section_title), FadeOut(full_diagram))

    def show_config_system(self):
        section_title = Text("5. Configuration System", font_size=36, color=YELLOW)
        self.play(Write(section_title))
        self.wait(1)
        self.play(section_title.animate.to_edge(UP))

        # --- Construct all components FIRST, without animating ---

        # Configuration sources
        sources = VGroup()

        # Environment variables
        env_box = Rectangle(width=3, height=1, color=GREEN).set_fill(GREEN, opacity=0.2)
        env_label = Text("Environment Variables", font_size=16)
        env_group = VGroup(env_box, env_label)

        # .env file
        dotenv_box = Rectangle(width=3, height=1, color=BLUE).set_fill(BLUE, opacity=0.2)
        dotenv_label = Text(".env File", font_size=16)
        dotenv_group = VGroup(dotenv_box, dotenv_label).next_to(env_group, RIGHT, buff=1)

        # Dotfiles
        dotfile_box = Rectangle(width=3, height=1, color=PURPLE).set_fill(PURPLE, opacity=0.2)
        dotfile_label = Text("Dotfiles (~/.api-*, ~/.model-*)", font_size=16)
        dotfile_group = VGroup(dotfile_box, dotfile_label).next_to(env_group, DOWN, buff=1)

        # Default values
        default_box = Rectangle(width=3, height=1, color=ORANGE).set_fill(ORANGE, opacity=0.2)
        default_label = Text("Default Values", font_size=16)
        default_group = VGroup(default_box, default_label).next_to(dotfile_group, RIGHT, buff=1)

        sources.add(env_group, dotenv_box, dotfile_box, default_box)

        # Priority arrows
        arrow1 = Arrow(env_group.get_right(), dotenv_group.get_left(), color=YELLOW, stroke_width=4)
        arrow2 = Arrow(dotenv_group.get_bottom(), dotfile_group.get_top(), color=YELLOW, stroke_width=4)
        arrow3 = Arrow(dotfile_group.get_right(), default_group.get_left(), color=YELLOW, stroke_width=4)

        # Priority labels
        priority1 = Text("1st Priority", font_size=14, color=YELLOW).next_to(arrow1, UP)
        priority2 = Text("2nd Priority", font_size=14, color=YELLOW).next_to(arrow2, LEFT)
        priority3 = Text("3rd Priority", font_size=14, color=YELLOW).next_to(arrow3, UP)

        # Config loading process
        config_process = Rectangle(width=5, height=2, color=RED).set_fill(RED, opacity=0.2)
        config_text = Text("Pydantic Config Loading", font_size=18).next_to(config_process, UP)
        config_code = Text(
            """class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        frozen=True,
        extra="ignore"
    )""",
            font_size=14,
            font="monospace"
        )

        config_group = VGroup(config_process, config_text, config_code).next_to(default_group, DOWN, buff=1.5)

        # --- Create the MASTER GROUP ---
        full_diagram = VGroup(
            env_group, dotenv_group, dotfile_group, default_group,
            arrow1, arrow2, arrow3, priority1, priority2, priority3, config_group
        )

        # --- Scale and Position the Master Group ---
        full_diagram.scale(0.8).next_to(section_title, DOWN, buff=0.3)

        # --- Animate ---
        self.play(FadeIn(full_diagram))
        self.wait(3)
        self.play(FadeOut(section_title), FadeOut(full_diagram))

    def show_conclusion(self):
        conclusion_title = Text("Conclusion", font_size=36, color=GREEN)
        self.play(Write(conclusion_title))
        self.wait(1)

        features = VGroup()

        feature1 = Text("✓ Modular FastMCP architecture", font_size=24, color=BLUE)
        feature2 = Text("✓ Multi-provider AI support (OpenRouter + Gemini)", font_size=24, color=BLUE)
        feature3 = Text("✓ SQLite database with connection pooling", font_size=24, color=BLUE)
        feature4 = Text("✓ Flexible configuration system", font_size=24, color=BLUE)
        feature5 = Text("✓ Comprehensive user and dialog management", font_size=24, color=BLUE)
        feature6 = Text("✓ Production-ready with proper error handling", font_size=24, color=BLUE)

        features = VGroup(feature1, feature2, feature3, feature4, feature5, feature6).arrange(DOWN, buff=0.3)

        self.play(Write(features))

        self.wait(3)

        # Final message
        final_msg = Text("MCP Waifu Chat Server - Ready for deployment!", font_size=32, color=YELLOW)
        final_msg.next_to(features, DOWN, buff=1)

        self.play(Write(final_msg))

        self.wait(2)

        self.play(FadeOut(conclusion_title), FadeOut(features), FadeOut(final_msg))

# To run this animation:
# manim -pql manim-animation.py MCPWaifuChatExplanation