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
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                        <CardActionArea onClick={() => onResultClick(result.doc_id)} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', alignItems: 'flex-start', p: 1 }}>
                            <CardContent sx={{ width: '100%' }}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                    <Typography variant="subtitle2" sx={{ color: 'primary.main', fontWeight: 600 }}>
                                        DOC-{result.doc_id}
                                    </Typography>
                                    <Chip
                                        label={`${(result.score * 100).toFixed(0)}% Match`}
                                        size="small"
                                        color={result.score > 0.7 ? "success" : "primary"}
                                        variant="filled"
                                        sx={{ borderRadius: 1, fontWeight: 600 }}
                                    />
                                </Box>
                                <Typography variant="body2" color="text.secondary" sx={{
                                    display: '-webkit-box',
                                    WebkitLineClamp: 4,
                                    WebkitBoxOrient: 'vertical',
                                    overflow: 'hidden',
                                    lineHeight: 1.6
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
