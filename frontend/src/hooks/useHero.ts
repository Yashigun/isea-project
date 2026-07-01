import { useEffect, useState } from "react";

import { getHero } from "@/services/hero";

import { Hero } from "@/types/hero";

export function useHero() {
  const [hero, setHero] = useState<Hero | null>(null);

  useEffect(() => {
    getHero().then(setHero);
  }, []);

  return hero;
}