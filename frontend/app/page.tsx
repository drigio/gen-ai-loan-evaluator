"use client"

import { useState } from "react"
import Dashboard from "../dashboard"
import UploadPage from "../upload-page"

export default function SyntheticV0PageForDeployment() {
  const [showDashboard, setShowDashboard] = useState(false);
  const [applicantId, setApplicantId] = useState<string | null>(null); // applicantId can be null initially

  const handleAnalysisComplete = (applicantId: string) => { // Updated: accepts applicantId
    setApplicantId(applicantId); // set applicantId state
    setShowDashboard(true);
  };

  const handleReset = () => {
    setShowDashboard(false);
    setApplicantId(null); // Reset applicantId when going back to upload page
  };

  return (
    <>
      <div
        className={`transition-opacity duration-700 ease-in-out ${
          showDashboard ? "opacity-0" : "opacity-100"
        }`}
      >
        {!showDashboard && (
          <UploadPage onAnalysisComplete={handleAnalysisComplete} /> // pass updated handleAnalysisComplete
        )}
      </div>
      <div
        className={`transition-opacity duration-700 ease-in-out absolute top-0 left-0 w-full h-full ${
          showDashboard ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
      >
        {showDashboard && (
          <Dashboard applicantId={applicantId!} onReset={handleReset} /> // pass applicantId. ! is used as applicantId will not be null here
        )}
      </div>
    </>
  );
}