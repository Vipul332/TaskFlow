
import NotificationsClient from "./NotificationsClient";

// This page uses authenticated, client-side notification data.
// Allow this route to block during navigation.
export const instant = false;

export default function NotificationsPage() {
  return <NotificationsClient />;
}
