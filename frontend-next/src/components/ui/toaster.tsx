"use client";

import { useState, useCallback } from "react";
import { ToastProvider, ToastViewport, Toast, ToastTitle, ToastDescription, ToastClose } from "./toast";

interface ToastData {
  id: string;
  title: string;
  description?: string;
  variant?: "default" | "success" | "destructive";
}

let toastQueue: ((t: ToastData) => void) | null = null;

export function toast(data: Omit<ToastData, "id">) {
  toastQueue?.({ ...data, id: Date.now().toString() });
}

export function Toaster() {
  const [toasts, setToasts] = useState<ToastData[]>([]);

  const addToast = useCallback((t: ToastData) => {
    setToasts((prev) => [...prev, t]);
    setTimeout(() => setToasts((prev) => prev.filter((p) => p.id !== t.id)), 4000);
  }, []);

  toastQueue = addToast;

  return (
    <ToastProvider>
      {toasts.map((t) => (
        <Toast key={t.id} variant={t.variant} open>
          <div className="flex-1">
            <ToastTitle>{t.title}</ToastTitle>
            {t.description && <ToastDescription>{t.description}</ToastDescription>}
          </div>
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProvider>
  );
}
