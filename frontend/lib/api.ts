export async function fetchApplicantData(applicantId: string) {
    const response = await fetch(`http://localhost:8001/applicants/${applicantId}`);
    if (!response.ok) {
        if (response.status === 404) {
            return null;
        }
        throw new Error(`Failed to fetch applicant data: ${response.status}`);
    }
    const data = await response.json();
    return data;
}