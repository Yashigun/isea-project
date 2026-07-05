export interface Category {
  public_id: string;
  name: string;
  slug: string;
  description: string | null;
  image?: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
