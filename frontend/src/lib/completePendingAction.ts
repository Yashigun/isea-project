import { auth } from "@/services/auth";
import { cart } from "@/services/cart";
import { wishlist } from "@/services/wishlist";

import {
  getPendingAction,
  clearPendingAction,
} from "./authRedirect";

export async function completePendingAction() {
  const pending = getPendingAction();

  if (!pending) return;

  switch (pending.type) {
    case "wishlist":
      await wishlist.add(pending.payload.productId);
      break;

    case "cart":
      await cart.add(pending.payload.productId, pending.payload.quantity);
      break;

    case "checkout":
      break;

    default:
      break;
  }

  clearPendingAction();
}