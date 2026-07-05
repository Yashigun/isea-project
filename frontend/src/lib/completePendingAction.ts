import { auth } from "@/services/auth";
import { cartService } from "@/services/cart";
import { wishlistService } from "@/services/wishlist";

import {
  getPendingAction,
  clearPendingAction,
} from "./authRedirect";

export async function completePendingAction() {
  const pending = getPendingAction();

  if (!pending) return;

  switch (pending.type) {
    case "wishlist":
      await wishlistService.add(pending.payload.productId);
      break;

    case "cart":
      await cartService.addItem(pending.payload.productId, pending.payload.quantity);
      break;

    case "checkout":
      break;

    default:
      break;
  }

  clearPendingAction();
}