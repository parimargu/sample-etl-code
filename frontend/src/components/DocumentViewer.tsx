import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, CircularProgress } from '@mui/material';
import { Document } from '../services/api';

interface DocumentViewerProps {
    open: boolean;
    onClose: () => void;
    document: Document | null;
    loading: boolean;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ open, onClose, document, loading }) => {
    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>Document Viewer</DialogTitle>
            <DialogContent dividers>
                {loading ? (
                    <CircularProgress />
                ) : document ? (
                    <>
                        <Typography variant="h6" gutterBottom>
                            ID: {document.doc_id}
                        </Typography>
                        <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                            {document.text}
                        </Typography>
                    </>
                ) : (
                    <Typography>No document selected</Typography>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
};

export default DocumentViewer;
