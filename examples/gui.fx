use gui;

fn build_ui(win) {
    gui_label(win, "Hello from Fluxia GUI!");
    gui_button(win, "Click me", "on_click");
}

fn on_click() {
    print("Button clicked!");
}

fn main() {
    gui_app("Fluxia GUI Demo", "build_ui");
}
