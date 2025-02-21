// Filename: app/upload-page.tsx
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Upload, ArrowRight, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { LoadingOverlay } from "@/components/ui/loading-overlay"
import { Separator } from "./components/ui/separator"

interface UploadPageProps {
    onAnalysisComplete: (applicantId: string) => void; // Updated prop type to accept applicantId
}

export default function UploadPage({ onAnalysisComplete }: UploadPageProps) {
    const [file, setFile] = useState<File | null>(null)
    const [isUploading, setIsUploading] = useState(false)
    const router = useRouter()

    async function handleUpload(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        if (!file) return

        setIsUploading(true)

        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("http://localhost:8002/api/v1/process-bank-statement", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                const applicantId = data.applicant_id;
                onAnalysisComplete(applicantId); // Call the callback function with applicantId from API
            } else {
                console.error("Bank statement processing failed:", response.status, response.statusText);
                console.log(response);
                // Optionally display user-friendly error message here
            }
        } catch (error) {
            console.error("Upload failed:", error);
            
            // Optionally display user-friendly error message here
        } finally {
            setIsUploading(false);
        }
    }

    return (

        <div className="min-h-screen bg-slate-50 bg-[url('/bg.png')] bg-repeat">
            <header className="top-0 z-0 w-full border-b border-border/40 bg-header-dark text-white">
                <div className="px-24 h-32 flex max-w-screen items-center">
                    <div className="hidden md:flex">
                        <a className="flex items-center" href="/">
                            <span className="font-sans hidden font-bold sm:inline-block text-3xl subpixel-antialiased ">SaraFi</span>
                        </a>
                    </div>
                </div>
                {/* <div className="mx-24 pb-4">
                    <Separator className="mb-6 bg-gray-700 " />
                </div> */}
            </header>

            <main className="container mx-auto px-4 py-24">
                <Card className="mx-auto max-w-2xl bg-main-light">
                    <CardContent className="p-8">
                        <h1 className="mb-8 text-3xl font-semibold tracking-tight">Upload your bank statement</h1>

                        <form onSubmit={handleUpload} className="space-y-6">
                            <div className="rounded-lg border-2 border-dashed border-gray-200 p-8 text-center">
                                {file ? (
                                    <div className="space-y-2">
                                        <p className="text-sm font-medium">{file.name}</p>
                                        <Button type="button" variant="outline" onClick={() => setFile(null)}>
                                            Choose different file
                                        </Button>
                                    </div>
                                ) : (
                                    <label className="cursor-pointer space-y-4">
                                        <div className="flex justify-center">
                                            <div className="rounded-full bg-blue-50 p-4">
                                                <Upload className="h-8 w-8 text-blue-600" />
                                            </div>
                                        </div>
                                        <div>
                                            <p className="text-base font-medium">Drop your bank statement here</p>
                                            <p className="text-sm text-gray-500">or click to browse (PDF only)</p>
                                        </div>
                                        <input
                                            type="file"
                                            className="hidden"
                                            accept=".pdf"
                                            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                                        />
                                    </label>
                                )}
                            </div>

                            <div className="flex justify-end">
                                <Button
                                    type="submit"
                                    className="min-w-[120px] bg-blue-600 hover:bg-blue-700"
                                    disabled={!file || isUploading}
                                >
                                    {isUploading ? (
                                        <>
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                            Analyzing
                                        </>
                                    ) : (
                                        <>
                                            Analyze
                                            <ArrowRight className="ml-2 h-4 w-4" />
                                        </>
                                    )}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>

                {isUploading && <LoadingOverlay />}
            </main>

            <footer className="fixed bottom-0 left-0 right-0 border-t bg-main-light p-8">
                <div className="container mx-auto flex items-center justify-center gap-4 text-sm text-gray-600">
                </div>
            </footer>
        </div>
    )
}