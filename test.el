(require 'json)
(require 'shr)

(global-set-key (kbd "<f7>") 'get-token-definition)



(defun get-token-definition ()
  (interactive)
  (let* ((aa (thing-at-point 'word 'no-properties))
	 
	 )
(message aa)
    )

  )
