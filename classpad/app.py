from __future__ import annotations

import logging
import sys
from pathlib import Path


def main() -> None:
    log_path = Path.home() / ".open-classpad.log"
    logging.basicConfig(filename=log_path, level=logging.ERROR,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        from classpad.ui.shell import ClassPadShell
        ClassPadShell().mainloop()
    except Exception:
        logging.exception("Fatal application error")
        try:
            from tkinter import messagebox
            messagebox.showerror("Open ClassPad", f"An unexpected error occurred.\nDetails: {log_path}")
        except Exception:
            print(f"Open ClassPad failed. See {log_path}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
