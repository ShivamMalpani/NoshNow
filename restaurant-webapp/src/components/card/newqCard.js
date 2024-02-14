import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Button, CardActionArea, CardActions } from '@mui/material';

export default function MultiActionAreaCard({name,cost,quantity,imageUrl}) {
  return (
    <Card  sx={{ maxWidth: 345, margin:5, paddingTop:5, paddingLeft:3, paddingRight:3 }}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="140"
          image={imageUrl}
          alt="green iguana"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            <p>Cost: ₹ {cost}</p>
            <p>Quantity: {quantity}</p>
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          Update Item
        </Button>
      </CardActions>
    </Card>
  );
}