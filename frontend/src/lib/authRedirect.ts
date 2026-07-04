import { useRouter } from "next/navigation";

export interface PendingAction {
  type: string;
  payload?: any;
}

export function savePendingAction(
  action: PendingAction,
  returnUrl: string = window.location.pathname + window.location.search
) {
  sessionStorage.setItem("returnUrl", returnUrl);
  sessionStorage.setItem("pendingAction", JSON.stringify(action));
}

export function getPendingAction(): PendingAction | null {
  const item = sessionStorage.getItem("pendingAction");

  if (!item) return null;

  return JSON.parse(item);
}

export function clearPendingAction() {
  sessionStorage.removeItem("pendingAction");
}

export function getReturnUrl() {
  return sessionStorage.getItem("returnUrl") || "/";
}

export function clearReturnUrl() {
  sessionStorage.removeItem("returnUrl");
}