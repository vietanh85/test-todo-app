# ADR-007: Natural Anonymization Strategy for ADAS Training Data

## Status
Proposed

## Context
Data collected from vehicles for ADAS training contains Personally Identifiable Information (PII), primarily human faces and vehicle license plates. Compliance with global privacy regulations (GDPR, APPI, CCPA) requires this data to be anonymized before it can be used by AI researchers or stored long-term. 

Traditional techniques like **Gaussian blurring** or **pixelation** destroy the structural integrity of the image. For ADAS training, it is crucial to preserve the semantic context (e.g., "where is the person looking?", "what is the orientation of the license plate?") to train robust detection and behavior prediction models.

## Decision
We will implement **Natural Anonymization** (Generative In-painting) using a **Selective Processing** strategy as the primary anonymization approach for the NOA DataOps platform.

Key components of the decision:
1. **Detection:** Use a high-precision object detection model (e.g., specialized YOLO or EfficientDet) to identify all faces and license plates in every frame.
2. **Generative Overlay:** Instead of blurring, use a Generative Adversarial Network (GAN) or Stable Diffusion-based model to replace the detected PII with realistic, AI-generated synthetic alternatives that match the lighting, pose, and resolution of the original image.
3. **Selective Anonymization:** To optimize GPU compute resources, anonymization is triggered only for data clips tagged as "high-value" or when a dataset is requested for AI training.
4. **Metadata Preservation:** The original bounding box and semantic attributes (e.g., "Adult", "Walking") are preserved as metadata in the Silver/Gold layers.
5. **Fallback Mechanism:** If the confidence of the detection or generation is below a threshold, the system will fallback to traditional blurring to ensure compliance.
6. **Irreversibility:** The process is applied in the Silver layer, and the original "Raw" data is restricted to a highly secure, air-gapped "Landing" zone with strict access controls and a 30-day deletion policy.

## Consequences
### Positive
- **Training Fidelity:** Models trained on naturally anonymized data perform significantly better than those trained on blurred data because the visual context is preserved.
- **Privacy Compliance:** Meets "Privacy by Design" requirements while enabling data utility.
- **Data Longevity:** Reduced risk of future "re-identification" attacks compared to simple blurring.

### Negative
- **Computational Cost:** Natural anonymization is extremely GPU-intensive compared to simple blurring.
- **Processing Latency:** Increases the time from data ingestion to "Ready for Training" status.
- **Storage Overhead:** Requires storing both the transformed images and the metadata describing the transformations.

### Risks
- **Artifact Generation:** AI-generated faces might introduce "uncanny valley" artifacts that could bias the training models.
- **False Negatives:** If the detection model misses a PII instance, the system fails to comply with privacy laws.
- **Regulatory Uncertainty:** Some regulators may still prefer traditional blurring over AI-generated overlays; requires continuous legal review.
