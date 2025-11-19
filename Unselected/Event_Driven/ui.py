# ui.py
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from event_bus import EventBus
from events import (
    SceneId, ItemId,
    SceneChangeRequested, ItemUseRequested,
    SceneChanged, PlotAdvanced, ItemAcquired, ItemUsed,
)
from game_state import GameState


class UI:
    def __init__(self, bus: EventBus, state: GameState):
        self.bus = bus
        self.state = state

        self.root = tk.Tk()
        self.root.title("Event-Driven Adventure")
        self.root.geometry("860x560")
        self.root.update_idletasks()
        self.root.geometry("860x560+200+200")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(120, lambda: self.root.attributes("-topmost", False))

        self._build_layout()

        bus.subscribe(PlotAdvanced, self._on_plot_advanced)
        bus.subscribe(SceneChanged, self._on_scene_changed)
        bus.subscribe(ItemAcquired, self._on_inv_change)
        bus.subscribe(ItemUsed, self._on_inv_change)

        self._refresh_scene()
        self._refresh_inventory()
        self._refresh_actions()

    # ---------- Layout ----------
    def _build_layout(self):
        left = ttk.Frame(self.root, padding=8)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Story / Dialog", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        frm_text = ttk.Frame(left)
        frm_text.pack(fill=tk.BOTH, expand=True)
        self.txt_dialog = tk.Text(frm_text, wrap="word", state="disabled")
        scroll = ttk.Scrollbar(frm_text, command=self.txt_dialog.yview)
        self.txt_dialog.configure(yscrollcommand=scroll.set)
        self.txt_dialog.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        right = ttk.Frame(self.root, padding=8)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Scene ---
        frm_scene = ttk.LabelFrame(right, text="Scenes")
        frm_scene.pack(fill=tk.X)
        self.lbl_scene = ttk.Label(frm_scene, text="Current Location:")
        self.lbl_scene.pack(anchor="w", padx=8, pady=4)

        btns = ttk.Frame(frm_scene)
        btns.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btns, text="Town", command=lambda: self._go(SceneId.TOWN)).grid(row=0, column=0, sticky="ew", padx=4)
        ttk.Button(btns, text="Forest", command=lambda: self._go(SceneId.FOREST)).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(btns, text="Ruins", command=lambda: self._go(SceneId.RUINS)).grid(row=0, column=2, sticky="ew", padx=4)
        for i in range(3):
            btns.grid_columnconfigure(i, weight=1)

        # --- Actions ---
        frm_actions = ttk.LabelFrame(right, text="Actions")
        frm_actions.pack(fill=tk.X, pady=6)
        self.frm_actions = frm_actions

        # --- Inventory ---
        frm_inv = ttk.LabelFrame(right, text="Inventory")
        frm_inv.pack(fill=tk.BOTH, expand=True)
        self.list_inv = tk.Listbox(frm_inv)
        self.list_inv.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.list_inv.bind("<Double-1>", self._on_inv_double)

    # ---------- Event emit ----------
    def _go(self, scene):
        self.bus.publish(SceneChangeRequested(scene))

    def _use_item(self, item):
        self.bus.publish(ItemUseRequested(item))

    # ---------- Event callbacks ----------
    def _on_plot_advanced(self, ev):
        self._write(ev.text)
        self._refresh_actions()

    def _on_scene_changed(self, ev):
        self._refresh_scene()
        self._refresh_actions()

    def _on_inv_change(self, ev):
        self._refresh_inventory()
        self._refresh_actions()

    # ---------- Refresh UI ----------
    def _refresh_scene(self):
        title = self.state.get_scene_title()
        self.lbl_scene.config(text=f"Current Location: {title}")

    def _refresh_inventory(self):
        self.list_inv.delete(0, tk.END)
        if not self.state.inventory:
            self.list_inv.insert(tk.END, "(Empty)")
            return
        for it, qty in self.state.inventory.items():
            self.list_inv.insert(tk.END, f"{self.state.item_title(it)} x {qty}")

    def _refresh_actions(self):
        for w in self.frm_actions.winfo_children():
            w.destroy()

        s = self.state
        scene = s.current_scene

        def add(label, cmd):
            ttk.Button(self.frm_actions, text=label, command=cmd).pack(fill=tk.X, padx=6, pady=3)

        if scene == SceneId.FOREST:
            if not s.has_item(ItemId.KEY) and s.get_flag("key_hint_shown"):
                add("Pick up Ancient Key", lambda: self.bus.publish(
                    ItemAcquired(item=ItemId.KEY, source="forest")))
            add("Return to Town", lambda: self.bus.publish(
                SceneChangeRequested(SceneId.TOWN)))

        elif scene == SceneId.RUINS:
            if not s.get_flag("ruins_gate_open") and s.has_item(ItemId.KEY):
                add("Use Ancient Key to Unlock Gate",
                    lambda: self.bus.publish(ItemUseRequested(ItemId.KEY)))

    # ---------- Dialog ----------
    def _write(self, text):
        self.txt_dialog.configure(state="normal")
        self.txt_dialog.insert(tk.END, text + "\n")
        self.txt_dialog.see(tk.END)
        self.txt_dialog.configure(state="disabled")

    # ---------- Inventory double-click ----------
    def _on_inv_double(self, _):
        idx = self.list_inv.curselection()
        if not idx:
            return

        label = self.list_inv.get(idx[0])
        if label == "(Empty)":
            return

        name = label.split(" x ")[0]
        target = None

        for iid in ItemId:
            if self.state.item_title(iid) == name:
                target = iid
                break

        if not target:
            messagebox.showinfo("Notice", "Unknown item.")
            return

        self._use_item(target)

    def run(self):
        self.bus.publish(SceneChanged(new_scene=self.state.current_scene, prev_scene=None))
        self.root.mainloop()
