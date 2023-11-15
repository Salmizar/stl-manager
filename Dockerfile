# RUN FIRST
# npm run build

FROM node:18-alpine

COPY ["dist", "."]

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

EXPOSE 3000

ENTRYPOINT ["node", "index.html"]
