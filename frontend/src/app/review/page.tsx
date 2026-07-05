import Container from "@/components/layout/Container";
import Section from "@/components/ui/Section";
import SectionHeading from "@/components/common/SectionHeading";
import ShopReviews from "@/components/ShopReviews";
import { reviewService } from "@/services/review";

export default async function ReviewPage() {
  const reviews = await reviewService.listAll();

  return (
    <Section>
      <Container className="max-w-3xl">
        <SectionHeading
          title="Reviews"
          subtitle="All customer reviews."
        />
        <ShopReviews reviews={reviews} />
      </Container>
    </Section>
  );
}
