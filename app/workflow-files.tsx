"use client";

import { createContext, useContext, useMemo, useState } from "react";
import type { WorkflowRunResponse } from "./flowfoundry-api";

export type WorkflowFile = {
 id: string;
 file: File;
 addedFrom: "Initial request" | "Working session";
 sourceId?: string;
};

type WorkflowFilesContextValue = {
 files: WorkflowFile[];
 addFiles: (files: File[], addedFrom: WorkflowFile["addedFrom"]) => void;
 removeFile: (id: string) => void;
 clearFiles: () => void;
 markUploaded: (id: string, sourceId: string) => void;
 sessionId: string | null;
 setSessionId: (sessionId: string | null) => void;
 workflowRun: WorkflowRunResponse | null;
 setWorkflowRun: (run: WorkflowRunResponse | null) => void;
};

const WorkflowFilesContext = createContext<WorkflowFilesContextValue | null>(null);

const fileId = (file: File) => `${file.name}-${file.size}-${file.lastModified}`;

export function WorkflowFilesProvider({ children }: { children: React.ReactNode }) {
 const [files, setFiles] = useState<WorkflowFile[]>([]);
 const [sessionId, setSessionId] = useState<string | null>(null);
 const [workflowRun, setWorkflowRun] = useState<WorkflowRunResponse | null>(null);

 const value = useMemo<WorkflowFilesContextValue>(() => ({
  files,
  addFiles: (selectedFiles, addedFrom) => setFiles(current => {
   const next = [...current];
   for (const file of selectedFiles) {
    const id = fileId(file);
    if (!next.some(item => item.id === id)) next.push({ id, file, addedFrom });
   }
   return next;
  }),
  removeFile: id => setFiles(current => current.filter(item => item.id !== id)),
  clearFiles: () => setFiles([]),
  markUploaded: (id, sourceId) => setFiles(current => current.map(item =>
   item.id === id ? { ...item, sourceId } : item
  )),
  sessionId,
  setSessionId,
  workflowRun,
  setWorkflowRun,
 }), [files, sessionId, workflowRun]);

 return <WorkflowFilesContext.Provider value={value}>{children}</WorkflowFilesContext.Provider>;
}

export function useWorkflowFiles() {
 const context = useContext(WorkflowFilesContext);
 if (!context) throw new Error("useWorkflowFiles must be used within WorkflowFilesProvider");
 return context;
}
