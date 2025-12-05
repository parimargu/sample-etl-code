import React from 'react';
import { Grid, Card, CardContent, Typography, CardActionArea, Chip } from '@mui/material';
import { SearchResult } from '../services/api';

interface ResultsGridProps {
    results: SearchResult[];
    onResultClick: (docId: string) => void;
}

const ResultsGrid: React.FC<ResultsGridProps> = ({ results, onResultClick }) => {
    return (
        <Grid container spacing={3}>
            {results.map((result) => (
                <Grid item xs={12} md={6} lg={4} key={result.chunk_id}>
                    <Card>
                        <CardActionArea onClick={() => onResultClick(result.doc_id)}>
                            <CardContent>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                    <Typography variant="subtitle2" color="text.secondary">
                                        Doc ID: {result.doc_id}
                                    </Typography>
                                    <Chip label={`Score: ${result.score.toFixed(2)}`} size="small" color="primary" variant="outlined" />
                                </Box>
                                <Typography variant="body2" color="text.secondary" sx={{
                                    display: '-webkit-box',
                                    WebkitLineClamp: 3,
                                    WebkitBoxOrient: 'vertical',
                                    overflow: 'hidden'
                                }}>
                                    {result.text}
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Grid>
            ))}
        </Grid>
    );
};

import { Box } from '@mui/material';
export default ResultsGrid;
