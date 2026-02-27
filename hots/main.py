import threading
from datetime import datetime
from typing import List

import customtkinter as ctk

from discovery import build_host_queue
from payloads import build_all_payloads_for_host
from scanner import HostScanResult, scan_hosts_parallel
from netcheck import run_basic_network_checks
from stealth import StealthConfig
from validation import normalize_hosts, normalize_proxies


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("VPN Helper Scanner (Educational)")
        self.geometry("1000x650")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self._build_widgets()

        self.results: List[HostScanResult] = []

    def _build_widgets(self) -> None:
        # Top frame: domain input + controls
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.domain_entry = ctk.CTkEntry(top, width=260, placeholder_text="domain เช่น ais.co.th")
        self.domain_entry.pack(side="left", padx=(5, 5))

        self.scan_type_var = ctk.StringVar(value="websocket")
        self.ws_radio = ctk.CTkRadioButton(top, text="WebSocket", variable=self.scan_type_var, value="websocket")
        self.ws_radio.pack(side="left", padx=5)
        self.direct_radio = ctk.CTkRadioButton(top, text="Direct/SSL", variable=self.scan_type_var, value="direct")
        self.direct_radio.pack(side="left", padx=5)

        self.start_btn = ctk.CTkButton(top, text="Scan Auto", command=self.start_scan_thread)
        self.start_btn.pack(side="left", padx=10)

        self.net_test_btn = ctk.CTkButton(top, text="Quick Net Test", command=self.start_net_test_thread)
        self.net_test_btn.pack(side="left", padx=5)

        # Options frame: proxy + timeout
        options = ctk.CTkFrame(self)
        options.pack(fill="x", padx=10, pady=(0, 5))

        proxy_label = ctk.CTkLabel(options, text="Proxy list (ip:port,ip:port) - ว่างได้")
        proxy_label.pack(side="left", padx=(5, 5))

        self.proxy_entry = ctk.CTkEntry(
            options,
            width=360,
            placeholder_text="เช่น 104.18.5.238:8880,1.2.3.4:8080",
        )
        self.proxy_entry.pack(side="left", padx=(0, 10))

        self.timeout_value_label = ctk.CTkLabel(options, text="Timeout 4.0s")
        self.timeout_value_label.pack(side="left", padx=(0, 5))

        self.timeout_slider = ctk.CTkSlider(
            options,
            from_=3.0,
            to=5.0,
            number_of_steps=20,
            command=self._on_timeout_change,
        )
        self.timeout_slider.set(4.0)
        self.timeout_slider.pack(side="left", padx=(0, 5), fill="x", expand=True)

        # Custom hosts frame: manual list scanning
        custom = ctk.CTkFrame(self)
        custom.pack(fill="x", padx=10, pady=(0, 5))

        custom_label = ctk.CTkLabel(custom, text="Custom hosts list (ทีละบรรทัด)")
        custom_label.pack(anchor="w", padx=5, pady=(5, 0))

        self.custom_hosts_text = ctk.CTkTextbox(custom, height=70)
        self.custom_hosts_text.pack(side="left", fill="x", expand=True, padx=5, pady=(0, 5))

        buttons_frame = ctk.CTkFrame(custom)
        buttons_frame.pack(side="left", padx=5, pady=(0, 5))

        load_sample_btn = ctk.CTkButton(buttons_frame, text="Load Sample", command=self.on_load_sample_hosts, width=120)
        load_sample_btn.pack(fill="x", pady=(0, 5))

        self.custom_scan_btn = ctk.CTkButton(buttons_frame, text="Scan Custom List", command=self.start_custom_scan_thread, width=120)
        self.custom_scan_btn.pack(fill="x")

        # Middle frame: log (left) + results (right)
        middle = ctk.CTkFrame(self)
        middle.pack(fill="both", expand=True, padx=10, pady=5)

        log_frame = ctk.CTkFrame(middle)
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        log_label = ctk.CTkLabel(log_frame, text="Live Log")
        log_label.pack(anchor="w", padx=5, pady=(5, 0))

        self.log_text = ctk.CTkTextbox(log_frame)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        result_frame = ctk.CTkFrame(middle, width=300)
        result_frame.pack(side="right", fill="both", expand=False, padx=(5, 0))

        result_label = ctk.CTkLabel(result_frame, text="Hosts OK / WebSocket")
        result_label.pack(anchor="w", padx=5, pady=(5, 0))

        self.host_listbox = ctk.CTkTextbox(result_frame, width=260)
        self.host_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # คลิกบรรทัดเพื่อเลือก host ไปยังช่องด้านล่าง
        self.host_listbox.bind("<ButtonRelease-1>", self.on_host_click)

        save_btn = ctk.CTkButton(result_frame, text="Save Hosts", command=self.on_save_hosts)
        save_btn.pack(fill="x", padx=5, pady=(0, 5))

        # Bottom frame: payload preview + buttons
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=10, pady=(0, 10))

        self.selected_host_var = ctk.StringVar()
        self.selected_host_entry = ctk.CTkEntry(bottom, textvariable=self.selected_host_var, width=260, placeholder_text="เลือก host จากด้านขวา หรือกรอกเอง")
        self.selected_host_entry.pack(side="left", padx=5, pady=5)

        self.payload_type_var = ctk.StringVar(value="websocket")
        payload_ws = ctk.CTkRadioButton(bottom, text="Payload WebSocket", variable=self.payload_type_var, value="websocket")
        payload_ws.pack(side="left", padx=5)
        payload_direct = ctk.CTkRadioButton(bottom, text="Payload Direct", variable=self.payload_type_var, value="direct_patch")
        payload_direct.pack(side="left", padx=5)

        build_btn = ctk.CTkButton(bottom, text="Build Payload", command=self.on_build_payload)
        build_btn.pack(side="left", padx=5)

        copy_btn = ctk.CTkButton(bottom, text="Copy Payload", command=self.on_copy_payload)
        copy_btn.pack(side="left", padx=5)

        self.payload_text = ctk.CTkTextbox(self, height=140)
        self.payload_text.pack(fill="x", padx=10, pady=(0, 10))

    # --- Logging helpers -------------------------------------------------
    def log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {message}\n")
        self.log_text.see("end")

    def set_host_results(self, hosts: List[str]) -> None:
        self.host_listbox.delete("1.0", "end")
        for h in hosts:
            self.host_listbox.insert("end", h + "\n")

    def _on_timeout_change(self, value: float) -> None:
        self.timeout_value_label.configure(text=f"Timeout {value:.1f}s")


    def start_net_test_thread(self) -> None:
        self.net_test_btn.configure(state="disabled")
        self.log("เริ่มทดสอบเน็ตของเครื่องนี้ (Quick Net Test) ...")
        t = threading.Thread(target=self._net_test_flow, daemon=True)
        t.start()

    def _net_test_flow(self) -> None:
        try:
            timeout_val = float(self.timeout_slider.get())
            results = run_basic_network_checks(timeout=timeout_val)
            ok_count = 0
            for r in results:
                if r.ok:
                    ok_count += 1
                    self._safe_log(
                        f"[NET] {r.name} -> ok ({r.status_code}) {r.latency_ms:.0f}ms"
                    )
                else:
                    self._safe_log(
                        f"[NET] {r.name} -> error ({r.error}) {r.latency_ms:.0f}ms"
                    )
            self._safe_log(f"[NET] สรุปผ่าน {ok_count}/{len(results)} ปลายทาง")
        finally:
            self.after(0, lambda: self.net_test_btn.configure(state="normal"))

    # --- Scan workflow ---------------------------------------------------
    def start_scan_thread(self) -> None:
        domain = (self.domain_entry.get() or "").strip()
        if not domain:
            self.log("กรุณากรอกโดเมนก่อน")
            return

        self.start_btn.configure(state="disabled")
        self.results = []
        self.set_host_results([])
        self.log(f"เริ่มดึง subdomain สำหรับ {domain} ...")

        t = threading.Thread(target=self._scan_flow, args=(domain,), daemon=True)
        t.start()

    def _scan_flow(self, domain: str) -> None:
        try:
            hosts = build_host_queue(domain)
            if not hosts:
                self._safe_log("ไม่พบ subdomain จาก crt.sh / brute force")
                self._safe_enable_button()
                return

            self._safe_log(f"พบ host ทั้งหมด {len(hosts)} ตัว เตรียมสแกน ...")

            proxies_raw = (self.proxy_entry.get() or "").strip()
            proxies, invalid_proxies = normalize_proxies(proxies_raw)
            if invalid_proxies:
                self._safe_log(f"ข้าม proxy format ไม่ถูกต้อง: {', '.join(invalid_proxies)}")

            timeout_val = float(self.timeout_slider.get())
            cfg = StealthConfig(timeout=timeout_val, proxies=proxies or None)

            def on_progress(res: HostScanResult) -> None:
                msg = f"{res.host} -> {res.status}"
                if res.http_status:
                    msg += f" ({res.http_status})"
                if res.port:
                    msg += f" :{res.port}"
                self._safe_log(msg)

            scheme = "https"
            scan_type = self.scan_type_var.get()
            if scan_type == "direct":
                scheme = "http"

            results = scan_hosts_parallel(
                hosts=hosts,
                config=cfg,
                scheme=scheme,
                max_workers=10,
                proxies=proxies or None,
                on_progress=on_progress,
            )

            self.results = results
            good_hosts = [r.host for r in results if r.status in {"ok", "websocket"}]
            self._safe_log(f"สแกนเสร็จ สิทธิ์ผ่าน {len(good_hosts)} host")
            self._safe_set_hosts(good_hosts)
        finally:
            self._safe_enable_button()

    def start_custom_scan_thread(self) -> None:
        text = self.custom_hosts_text.get("1.0", "end").strip()
        hosts_raw = [line.strip() for line in text.splitlines() if line.strip()]
        hosts, invalid_hosts = normalize_hosts(hosts_raw)
        if invalid_hosts:
            self.log(f"ข้าม host format ไม่ถูกต้อง: {', '.join(invalid_hosts)}")
        if not hosts:
            self.log("กรุณาวางลิสต์ host ที่ถูกต้องอย่างน้อย 1 รายการ")
            return

        self.custom_scan_btn.configure(state="disabled")
        self.results = []
        self.set_host_results([])
        self.log(f"เริ่มสแกนจาก custom list ทั้งหมด {len(hosts)} host ...")

        t = threading.Thread(target=self._scan_custom_flow, args=(hosts,), daemon=True)
        t.start()

    def _scan_custom_flow(self, hosts: List[str]) -> None:
        try:
            self._safe_log(f"เตรียมสแกน custom hosts {len(hosts)} ตัว ...")

            proxies_raw = (self.proxy_entry.get() or "").strip()
            proxies, invalid_proxies = normalize_proxies(proxies_raw)
            if invalid_proxies:
                self._safe_log(f"ข้าม proxy format ไม่ถูกต้อง: {', '.join(invalid_proxies)}")

            timeout_val = float(self.timeout_slider.get())
            cfg = StealthConfig(timeout=timeout_val, proxies=proxies or None)

            def on_progress(res: HostScanResult) -> None:
                msg = f"{res.host} -> {res.status}"
                if res.http_status:
                    msg += f" ({res.http_status})"
                if res.port:
                    msg += f" :{res.port}"
                self._safe_log(msg)

            scheme = "https"
            scan_type = self.scan_type_var.get()
            if scan_type == "direct":
                scheme = "http"

            results = scan_hosts_parallel(
                hosts=hosts,
                config=cfg,
                scheme=scheme,
                max_workers=10,
                proxies=proxies or None,
                on_progress=on_progress,
            )

            self.results = results
            good_hosts = [r.host for r in results if r.status in {"ok", "websocket"}]
            self._safe_log(f"สแกน custom เสร็จ สิทธิ์ผ่าน {len(good_hosts)} host")
            self._safe_set_hosts(good_hosts)
        finally:
            self._safe_enable_custom_button()

    # --- Thread-safe UI updates ------------------------------------------
    def _safe_log(self, msg: str) -> None:
        self.after(0, lambda: self.log(msg))

    def _safe_set_hosts(self, hosts: List[str]) -> None:
        self.after(0, lambda: self.set_host_results(hosts))

    def _safe_enable_button(self) -> None:
        self.after(0, lambda: self.start_btn.configure(state="normal"))

    def _safe_enable_custom_button(self) -> None:
        self.after(0, lambda: self.custom_scan_btn.configure(state="normal"))

    # --- Payload actions --------------------------------------------------
    def on_load_sample_hosts(self) -> None:
        try:
            with open("sample_hosts.txt", "r", encoding="utf-8") as f:
                data = f.read().strip()
            self.custom_hosts_text.delete("1.0", "end")
            self.custom_hosts_text.insert("1.0", data + "\n")
            self.log("โหลด sample_hosts.txt เข้าช่อง Custom hosts list แล้ว")
        except FileNotFoundError:
            self.log("ไม่พบไฟล์ sample_hosts.txt ในโฟลเดอร์โปรเจกต์")
        except Exception as exc:  # noqa: BLE001
            self.log(f"โหลด sample hosts ไม่สำเร็จ: {exc}")

    def on_build_payload(self) -> None:
        host = (self.selected_host_var.get() or "").strip()
        if not host:
            # ถ้า text field ว่าง จะลองอ่านบรรทัดแรกจาก host_listbox
            all_text = self.host_listbox.get("1.0", "end").strip().splitlines()
            if all_text:
                host = all_text[0].strip()
                self.selected_host_var.set(host)

        if not host:
            self.log("ยังไม่ได้เลือก host สำหรับสร้าง payload")
            return

        all_payloads = build_all_payloads_for_host(host)
        key = self.payload_type_var.get()
        payload = all_payloads.get(key, "")
        self.payload_text.delete("1.0", "end")
        self.payload_text.insert("1.0", payload)

    def on_copy_payload(self) -> None:
        payload = self.payload_text.get("1.0", "end").strip()
        if not payload:
            self.log("ยังไม่มี payload ให้คัดลอก")
            return
        self.clipboard_clear()
        self.clipboard_append(payload)
        self.log("คัดลอก payload ไปที่คลิปบอร์ดแล้ว")

    def on_host_click(self, event) -> None:  # type: ignore[override]
        try:
            index = self.host_listbox.index(f"@{event.x},{event.y}")
            line = index.split(".")[0]
            host = self.host_listbox.get(f"{line}.0", f"{line}.end").strip()
            if host:
                self.selected_host_var.set(host)
        except Exception:
            return

    def on_save_hosts(self) -> None:
        text = self.host_listbox.get("1.0", "end").strip()
        if not text:
            self.log("ยังไม่มี host สำหรับบันทึก")
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hosts_{ts}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# Hosts saved at {datetime.now().isoformat()}\n")
                f.write(text + "\n")
            self.log(f"บันทึก hosts ลงไฟล์ {filename}")
        except Exception as exc:  # noqa: BLE001
            self.log(f"บันทึกไฟล์ไม่สำเร็จ: {exc}")


if __name__ == "__main__":
    app = App()
    app.mainloop()

