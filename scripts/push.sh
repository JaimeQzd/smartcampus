#!/bin/sh

#realizamos el push
git push "$@"

#guardamos el codigo de salida del push
PUSH_STATUS=$?

#si el push falla, da error
if [ $PUSH_STATUS -ne 0 ]; then
    echo "El push ha fallado."
    exit $PUSH_STATUS
fi

#si el push funciona, ejecutamos nuestro post-push
.githooks/post-push

exit 0